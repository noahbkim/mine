from django.db import models
from django.utils import timezone

TRANSACTIONS = {1: "acquired", 2: "removed", 3: "lost", 4: "recorded"}


class Location(models.Model):
    """A location where items can be."""

    name = models.CharField(max_length=128, unique=True, primary_key=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """A general category of items."""

    name = models.CharField(max_length=128, unique=True, primary_key=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Detail(models.Model):
    """A key-value pair describing an item."""

    name = models.CharField(max_length=64)
    value = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class PackingList(models.Model):
    """A reference list of owned items."""

    user = models.ForeignKey(to="auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    notes = models.TextField(null=True, blank=True)
    items = models.ManyToManyField(to="Item", through="PackingListInventory", related_name="+")

    def __str__(self):
        return f"{self.user.username}:{self.name}"


class PackingListInventory(models.Model):
    """A relational table for counting items in a packing list."""

    list = models.ForeignKey(to="PackingList", on_delete=models.CASCADE)
    item = models.ForeignKey(to="Item", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.list.name}:{self.item.name} ({self.count})"


class UserInventory(models.Model):
    """A relational table for counting items for a user."""

    user = models.ForeignKey(to="auth.User", on_delete=models.CASCADE)
    item = models.ForeignKey(to="Item", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}:{self.item.name} ({self.count})"


class Item(models.Model):
    """The core container of the inventory system."""

    users = models.ManyToManyField(to="auth.User", related_name="items", through="UserInventory")

    name = models.CharField(max_length=128)
    notes = models.TextField(null=True, blank=True)

    location = models.ForeignKey(to="Location", null=True, related_name="items", on_delete=models.SET_NULL)
    category = models.ForeignKey(to="Category", null=True, related_name="items", on_delete=models.SET_NULL)
    details = models.ManyToManyField(to="Detail", related_name="items")

    volume = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """A record of having acquired, removed, or lost an item."""

    item = models.ForeignKey(to="Item", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    mode = models.PositiveSmallIntegerField(choices=TRANSACTIONS.items())
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.item.name}:{TRANSACTIONS[self.mode]}"
