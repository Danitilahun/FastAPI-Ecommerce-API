from sqlalchemy.orm import Session
from app.models.models import Order, OrderItem, Product
from app.schemas.orders import OrderUpdate, OrderCreate  # Updated import
from app.utils.responses import ResponseHandler
from sqlalchemy.orm import joinedload
from app.core.security import get_current_user


class OrderService:  # Changed class name
    # Get All Orders (Changed naming to match)
    @staticmethod
    def get_all_orders(token, db: Session, page: int, limit: int):  # Changed method name
        user_id = get_current_user(token)
        orders = db.query(Order).filter(Order.user_id == user_id).offset((page - 1) * limit).limit(limit).all()  # Changed model name
        message = f"Page {page} with {limit} orders"  # Changed message
        return ResponseHandler.success(message, orders)

    # Get A Order By ID (Changed naming to match)
    @staticmethod
    def get_order(token, db: Session, order_id: int):  # Changed method name
        user_id = get_current_user(token)
        order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()  # Changed model name
        if not order:
            ResponseHandler.not_found_error("Order", order_id)  # Changed error message
        return ResponseHandler.get_single_success("order", order_id, order)

    # Create a new Order (Changed naming to match)
    @staticmethod
    def create_order(token, db: Session, order: OrderCreate):  # Changed method and parameter name
        user_id = get_current_user(token)
        order_dict = order.model_dump()

        order_items_data = order_dict.pop("order_items", [])  # Changed variable name
        order_items = []  # Changed variable name
        total_amount = 0
        for item_data in order_items_data:  # Changed variable name
            product_id = item_data['product_id']
            quantity = item_data['quantity']

            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return ResponseHandler.not_found_error("Product", product_id)

            subtotal = quantity * product.price * (product.discount_percentage / 100)
            order_item = OrderItem(product_id=product_id, quantity=quantity, subtotal=subtotal)  # Changed model and variable name
            total_amount += subtotal

            order_items.append(order_item)  # Changed variable name
        order_db = Order(order_items=order_items, user_id=user_id, total_amount=total_amount, **order_dict)  # Changed model name and variable name
        db.add(order_db)  # Changed variable name
        db.commit()
        db.refresh(order_db)  # Changed variable name
        return ResponseHandler.create_success("Order", order_db.id, order_db)  # Changed response message

    # Update Order & OrderItem (Changed naming to match)
    @staticmethod
    def update_order(token, db: Session, order_id: int, updated_order: OrderUpdate):  # Changed method and parameter names
        user_id = get_current_user(token)

        order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()  # Changed model name
        if not order:
            return ResponseHandler.not_found_error("Order", order_id)  # Changed error message

        # Delete existing order_items (Changed variable name)
        db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()  # Changed model name

        for item in updated_order.order_items:  # Changed variable name
            product_id = item.product_id
            quantity = item.quantity

            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return ResponseHandler.not_found_error("Product", product_id)

            subtotal = quantity * product.price * (product.discount_percentage / 100)

            order_item = OrderItem(  # Changed model name
                order_id=order_id,  # Changed variable name
                product_id=product_id,
                quantity=quantity,
                subtotal=subtotal
            )
            db.add(order_item)  # Changed variable name

        order.total_amount = sum(item.subtotal for item in order.order_items)  # Changed model name and variable name

        db.commit()
        db.refresh(order)  # Changed variable name
        return ResponseHandler.update_success("order", order.id, order)  # Changed response message

    # Delete Both Order and OrderItems (Changed naming to match)
    @staticmethod
    def delete_order(token, db: Session, order_id: int):  # Changed method name
        user_id = get_current_user(token)
        order = (  # Changed variable name
            db.query(Order)  # Changed model name
            .options(joinedload(Order.order_items).joinedload(OrderItem.product))  # Changed model and attribute names
            .filter(Order.id == order_id, Order.user_id == user_id)  # Changed model name
            .first()
        )
        if not order:
            ResponseHandler.not_found_error("Order", order_id)  # Changed error message

        for order_item in order.order_items:  # Changed model and variable name
            db.delete(order_item)  # Changed variable name

        db.delete(order)  # Changed variable name
        db.commit()
        return ResponseHandler.delete_success("Order", order_id, order)  # Changed response message