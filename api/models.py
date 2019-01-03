from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

TRANSACTIONS = {1: "acquired", 2: "removed", 3: "lost", 4: "recorded", 5: "consumed"}


class Session(models.Model):
    """A simple, token-based authentication strategy."""

    user = models.OneToOneField(to="auth.User", on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


class Location(models.Model):
    """A location where items can be."""

    user = models.ForeignKey(to="auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    notes = models.TextField(null=True, blank=True)
    current = models.BooleanField(default=False)

    items = models.ManyToManyField(to="Item", blank=True, through="LocationInventory", related_name="locations")

    def __str__(self):
        return self.name


class Category(models.Model):
    """A general category of items."""

    user = models.ForeignKey(to="auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Detail(models.Model):
    """A key-value pair describing an item."""

    name = models.CharField(max_length=64)
    value = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class List(models.Model):
    """A reference list of owned items."""

    user = models.ForeignKey(to="auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    notes = models.TextField(null=True, blank=True)
    items = models.ManyToManyField(to="Item", blank=True, through="ListInventory", related_name="lists")

    def __str__(self):
        return f"{self.user.username}:{self.name}"


class LocationInventory(models.Model):
    """A relational table for counting items at a location."""

    location = models.ForeignKey(to="Location", on_delete=models.CASCADE)
    item = models.ForeignKey(to="Item", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.location.name}:{self.item.name} ({self.count})"


class ListInventory(models.Model):
    """A relational table for counting items in a packing list."""

    list = models.ForeignKey(to="List", on_delete=models.CASCADE)
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

    category = models.ForeignKey(to="Category", null=True, blank=True, related_name="items", on_delete=models.SET_NULL)
    details = models.ManyToManyField(to="Detail", blank=True, related_name="items")

    volume = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """A record of having acquired, removed, or lost an item."""

    user = models.ForeignKey(to="auth.User", on_delete=models.CASCADE)
    item = models.ForeignKey(to="Item", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)

    mode = models.PositiveSmallIntegerField(choices=TRANSACTIONS.items())

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.item.name}:{TRANSACTIONS[self.mode]}"


class Movement(models.Model):
    """A record of moving one object to or from a location."""

    user = models.ForeignKey(to="auth.User", on_delete=models.CASCADE)
    item = models.ForeignKey(to="Item", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)

    source = models.ForeignKey(to="Location", on_delete=models.CASCADE, related_name="+")
    destination = models.ForeignKey(to="Location", on_delete=models.CASCADE, related_name="+")

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.item.name}:{self.source.name}->{self.destination.name}"
