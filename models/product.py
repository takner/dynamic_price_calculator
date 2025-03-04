from odoo import models, fields, api, _
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    # فیلد‌های جدید برای محاسبه قیمت
    price_in_dollar = fields.Float(string="قیمت به دلار", help="قیمت محصول به دلار")
    havale_fee = fields.Float(string="هزینه حواله", default=3500, help="هزینه دلار حواله‌ای به تومان")
    commission_percentage = fields.Float(string="درصد کارمزد", default=4.0, help="درصد کارمزد")
    last_updated_price = fields.Float(string="آخرین قیمت بروزرسانی شده", readonly=True)
    last_update_date = fields.Datetime(string="تاریخ آخرین بروزرسانی", readonly=True)
    
    @api.depends('price_in_dollar', 'havale_fee', 'commission_percentage')
    def _compute_price_in_currency(self):
        for product in self:
            try:
                # دریافت نرخ دلار از API
                response = requests.get('http://185.215.244.65:5001/prices', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    dollar_rate = data.get('dollar', 0)
                    
                    if dollar_rate > 0 and product.price_in_dollar > 0:
                        # محاسبه قیمت با احتساب نرخ دلار + هزینه حواله + کارمزد
                        base_price = product.price_in_dollar * (dollar_rate + product.havale_fee)
                        final_price = base_price * (1 + (product.commission_percentage / 100))
                        
                        # بروزرسانی قیمت محصول
                        product.list_price = final_price
                        product.last_updated_price = final_price
                        product.last_update_date = fields.Datetime.now()
            except Exception as e:
                # ثبت خطا در لاگ
                _logger.error(f"خطا در دریافت نرخ ارز: {e}")
    
    def update_all_prices(self):
        """تابع برای بروزرسانی قیمت همه محصولات"""
        products = self.search([('price_in_dollar', '>', 0)])
        products._compute_price_in_currency()
        return True


class PriceUpdateScheduler(models.Model):
    _name = 'price.update.scheduler'
    _description = 'زمانبندی بروزرسانی قیمت‌ها'
    
    @api.model
    def update_prices_cron(self):
        """تابع برای اجرا توسط کران جاب"""
        self.env['product.template'].update_all_prices()