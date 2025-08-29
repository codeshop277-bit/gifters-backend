from models import Gift

gifts_db: list[Gift] = [Gift(id= '1', name='test', size='M', color="Red")]

gifts_mock = [
        {"id": 1, "name": "Shirt", "brand": "Nike", "price": 40},
        {"id": 2, "name": "Cap", "brand": "Adidas", "price": 25},
        {"id": 3, "name": "Shoes", "brand": "Nike", "price": 90},
    ]

users_list = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com"
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob.smith@example.com"
    },
    {
        "id": 3,
        "name": "Charlie Brown",
        "email": "charlie.brown@example.com"
    }
]