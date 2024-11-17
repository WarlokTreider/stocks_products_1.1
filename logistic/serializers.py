from rest_framework import serializers
from django.db import transaction
from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = super().create(validated_data)

        # Создаем новые позиции на складе
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)

        return stock

    @transaction.atomic
    def update(self, instance, validated_data):
        # Извлекаем данные о позициях из валидированных данных
        positions_data = validated_data.pop('positions')

        # Обновляем поля склада (например, адрес)
        stock = super().update(instance, validated_data)

        # Собираем ID продуктов из входящих данных
        incoming_product_ids = [position['product'].id for position in positions_data]

        # Удаляем позиции, которых нет в списке входящих данных
        StockProduct.objects.filter(stock=stock).exclude(product_id__in=incoming_product_ids).delete()

        # Обновляем или создаем позиции
        for position_data in positions_data:
            product = position_data.get('product')
            quantity = position_data.get('quantity')
            price = position_data.get('price')

            # Используем update_or_create для обновления или создания новых записей
            StockProduct.objects.update_or_create(
                stock=stock,
                product=product,
                defaults={
                    'quantity': quantity,
                    'price': price,
                }
            )

        return stock
