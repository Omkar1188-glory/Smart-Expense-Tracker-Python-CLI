import uuid

class Transaction:
    def __init__(self, date, amount, type, category, description="", id=None):
        # If no ID provided, generate one automatically
        self.id = id or uuid.uuid4().hex
        self.date = date
        self.amount = float(amount)
        self.type = type
        self.category = category
        self.description = description

    def to_dict(self):
        """Return transaction data as dictionary (useful for saving later)"""
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "type": self.type,
            "category": self.category,
            "description": self.description,
        }

    def __str__(self):
        """Readable format when printed"""
        return (
            f"ID: {self.id}\n"
            f"Date: {self.date}\n"
            f"Amount: ₹{self.amount}\n"
            f"Type: {self.type}\n"
            f"Category: {self.category}\n"
            f"Description: {self.description}\n"
        )
