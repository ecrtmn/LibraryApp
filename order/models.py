from django.db import models, DataError, IntegrityError
from django.shortcuts import reverse
from authentication.models import CustomUser
from book.models import Book



class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='order')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    end_at = models.DateTimeField(null=True)
    planned_end_at = models.DateTimeField()

    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        :return: book id, book name, book description, book count, book authors
        """
        return str(self.to_dict())[1:-1]

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user,
            'book': self.book,
            'created_at': str(self.created_at),
            'end_at': str(self.end_at) if self.end_at else self.planned_end_at,
            'planned_end_at': str(self.planned_end_at)
        }

    @staticmethod
    def create(user, book, planned_end_at):
        try:
            order = Order(user=user, book=book, planned_end_at=planned_end_at)
            order.save()
        except (IntegrityError, DataError):
            pass
        else:
            return order

    @staticmethod
    def get_by_id(order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise Exception("Order does not exist.")
        else:
            return order

    def update(self, planned_end_at=None, end_at=None):
        if planned_end_at:
            self.planned_end_at = planned_end_at
        if end_at:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        all_orders = list(Order.objects.all())
        return all_orders

    @staticmethod
    def get_not_returned_books():
        not_returned = list(Order.objects.get(end_at=None))
        return not_returned

    @staticmethod
    def delete_by_id(order_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            obj = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            pass
        else:
            obj.delete()
            return True
        return False

    def get_absolute_url(self):
        return reverse('order_by_id', kwargs={'id': self.id})
