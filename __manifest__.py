{
    'name': 'Dynamic Price Calculator',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'محاسبه پویای قیمت محصولات بر اساس نرخ ارز',
    'description': """
        این ماژول قیمت محصولات را بر اساس نرخ لحظه‌ای دلار محاسبه می‌کند.
        - دریافت نرخ دلار از API
        - اضافه کردن هزینه حواله‌ای 
        - اعمال درصد کارمزد
    """,
    'author': 'KianKiaei',
    'depends': ['product', 'sale'],
    'data': [
        'views/product_view.xml',
        'data/cron.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}