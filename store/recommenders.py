from redis import StrictRedis

from django.conf import settings

from store.models import Product

# создаём соединение с базой данных Redis
redis_db = StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


class Recommender:

    @staticmethod
    def get_product_key(product_id):
        """
            формирует ключ для хранилиза Redis
        """
        return f'product:{product_id}:purchased_with'

    @staticmethod
    def get_product_ids(products):
        return [str(prd.pk) for prd in products]

    def products_bought(self, products):
        """
           добавляет товары купленные друг с другом
           и увеличивает их рейтинг
        """
        products_ids = self.get_product_ids(products)
        for product_id in products_ids:
            for with_id in products_ids:
                if product_id != with_id:
                    redis_db.zincrby(
                        name=self.get_product_key(product_id),
                        amount=1,
                        value=with_id
                    )

    def suggest_products_for(self, products, max_length=6):
        """
            если products == 1 то показывает рекоммендуемые товары для этого одного товара
            если их больше, то сохраняем аггрегированное значение этих товаров во временную переменную
            удаляем из этого аггрегированного значения товары, которые были переданы как аргумент функции
            и показываем это аггрегированное значение
        """
        if len(products) == 1:
            suggested_ids = redis_db.zrange(
                name=self.get_product_key(products[0].pk),  # 'product:{<id>}:purchased_with'
                start=0,  # от 0 индекса
                end=-1,  # до -1 индекса
                desc=True  # по убыванию
            )[:max_length]
        else:
            product_ids = self.get_product_ids(products)
            tmp_key = f'tmp_{"".join(product_ids)}'
            product_redis_keys = [
                self.get_product_key(product_id) for product_id in product_ids
            ]
            redis_db.zunionstore(  # аггрегирует значения переданных ключей и складывает их
                dest=tmp_key,
                keys=product_redis_keys,
            )
            redis_db.zrem(  # удаляет из множества Redis элементы, которые мы передали
                tmp_key,
                *product_ids
            )
            suggested_ids = redis_db.zrange(
                name=tmp_key,  # временный ключ в хранилище Redis по которому мы аггрегировали все значения
                start=0,  # от 0 индекса
                end=-1,  # до -1 индекса
                desc=True  # по убыванию
            )[:max_length]
            redis_db.delete(tmp_key)  # удаляем временный ключ, который больше нам не нужен

        suggested_ids = [int(prd_id) for prd_id in suggested_ids]
        suggested_products = list(Product.objects.filter(pk__in=suggested_ids))
        suggested_products.sort(
            key=lambda elem: suggested_ids.index(elem.pk)
        )
        return suggested_products

    def clear_purchases(self):
        """
            полностью очищает рекомендации для всех товаров
        """
        for product_id in self.get_product_ids(Product.objects.all()):
            redis_db.delete(self.get_product_key(product_id))
