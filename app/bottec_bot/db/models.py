from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.bottec_bot.db.session import Base

class TelegramResource(Base):
    __tablename__ = 'telegram_resources'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    tg_id = Column(String, nullable=False)
    

class FAQ(Base):
    __tablename__ = 'faqs'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Subcategory(Base):
    __tablename__ = 'subcategories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', backref='subcategories')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    photo_url = Column(String)
    price = Column(Integer, nullable=False)
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'))

    subcategory = relationship('Subcategory', backref='products')
    

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)

    product = relationship('Product')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    payment_status = Column(String, default='pending')  # 'pending', 'paid', 'failed'
