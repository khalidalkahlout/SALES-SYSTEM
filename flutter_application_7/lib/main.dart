import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const SmartStoreApp());
}

class SmartStoreApp extends StatelessWidget {
  const SmartStoreApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Smart Store',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: const Color(0xFFF5F5F5),
      ),
      home: const ProductsScreen(),
    );
  }
}

class ProductsScreen extends StatefulWidget {
  const ProductsScreen({super.key});

  @override
  State<ProductsScreen> createState() => _ProductsScreenState();
}

class _ProductsScreenState extends State<ProductsScreen> {
  // 1. دالة جلب المنتجات (GET)
  Future<List<dynamic>> fetchProducts() async {
    // 💡 ملاحظة: إذا كنت تستخدم إيموليتر أندرويد، استبدل 127.0.0.1 بـ 10.0.0.2
    final Uri url = Uri.parse('http://localhost:5000/products');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('فشل في تحميل البيانات من السيرفر');
      }
    } catch (e) {
      throw Exception('تأكد من تشغيل سيرفر البايثون: $e');
    }
  }

  // 2. دالة بيع المنتج وتحديث المخزن (POST)
  Future<void> sellProduct(int productId) async {
    final Uri url = Uri.parse('http://localhost:5000/sell_product/$productId');

    try {
      final response = await http.post(url);

      if (response.statusCode == 200) {
        // إعادة تحديث الشاشة فوراً لقراءة الكمية الجديدة من قاعدة البيانات
        setState(() {});

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('تمت عملية البيع وتحديث المخزن بنجاح! ✅'),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 2),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('عذراً، هذا المنتج نفذ من المخزن! ❌'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('حدث خطأ في الاتصال: $e'),
          backgroundColor: Colors.orange,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'مخزن المنتجات الذكي 📱',
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
        ),
        centerTitle: true,
        backgroundColor: Colors.blueAccent,
      ),
      body: FutureBuilder<List<dynamic>>(
        future: fetchProducts(), // جلب البيانات عند فتح الشاشة أو تحديثها
        builder: (context, snapshot) {
          // حالة التحميل
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          // حالة الخطأ (السيرفر مغلق أو المسار خاطئ)
          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text(
                  '❌ خطأ: ${snapshot.error}',
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.red,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            );
          }

          // عرض البيانات بعد النجاح
          final products = snapshot.data ?? [];
          if (products.isEmpty) {
            return const Center(child: Text('لا توجد منتجات في المخزن حالياً'));
          }

          return ListView.builder(
            itemCount: products.length,
            padding: const EdgeInsets.all(12),
            itemBuilder: (context, index) {
              final product = products[index];
              return Card(
                elevation: 4,
                margin: const EdgeInsets.symmetric(vertical: 8),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                child: ListTile(
                  contentPadding: const EdgeInsets.all(16),
                  leading: CircleAvatar(
                    backgroundColor: Colors.blue.shade100,
                    child: Text(
                      '${product['product_id']}',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                  ),
                  title: Text(
                    product['product_name'],
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  subtitle: Padding(
                    padding: const EdgeInsets.only(top: 8.0),
                    child: Text(
                      'القسم: ${product['category']} \nالمخزون المتاح: ${product['stock']} قطعة \nالسعر: ${product['price']} ج.م',
                      style: const TextStyle(
                        color: Colors.black87,
                        height: 1.3,
                      ),
                    ),
                  ),
                  // الزر التفاعلي الجديد
                  trailing: ElevatedButton.icon(
                    onPressed: () {
                      sellProduct(
                        product['product_id'],
                      ); // استدعاء دالة البيع والتحديث
                    },
                    icon: const Icon(
                      Icons.shopping_cart_checkout,
                      size: 18,
                      color: Colors.white,
                    ),
                    label: const Text(
                      'بيع قطعة',
                      style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 8,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
