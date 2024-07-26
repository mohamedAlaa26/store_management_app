# generate_ticket.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from models import Sale, Item, User, session, Ticket


def generate_ticket(sale_id):
    sale = session.query(Sale).filter_by(id=sale_id).first()
    item = session.query(Item).filter_by(id=sale.item_id).first()
    user = session.query(User).filter_by(id=sale.sold_by).first()

    if sale and item and user:
        c = canvas.Canvas(f"ticket_{sale_id}.pdf", pagesize=letter)
        c.drawString(100, 750, f"Sale ID: {sale.id}")
        c.drawString(100, 730, f"Item: {item.name}")
        c.drawString(100, 710, f"Description: {item.description}")
        c.drawString(100, 690, f"Quantity Sold: {sale.quantity_sold}")
        c.drawString(100, 670, f"Sale Date: {sale.sale_date}")
        c.drawString(100, 650, f"Total Price: {sale.total_price}")
        c.drawString(100, 630, f"Sold By: {user.username}")
        c.save()

        # Add ticket record to the database
        ticket = Ticket(sale_id=sale.id, ticket_data=f"ticket_{sale_id}.pdf")
        session.add(ticket)
        session.commit()


if __name__ == "__main__":
    generate_ticket(1)
