import wx
import os
from datetime import datetime

class FoodOrderApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="FoodZone", size=(1000, 700))
        
        self.cart = []
        self.user_email = ""
        self.is_admin = False
        self.selected_restaurant = None
        
        # Sample user database
        self.users = {
            "admin@food.com": {"password": "admin123", "is_admin": True},
            "user@food.com": {"password": "user123", "is_admin": False}
        }
        
        # Sample orders database
        self.all_orders = []
        
        # Restaurants data
        self.restaurants = {
            "Italian Bistro": {
                "items": [
                    {"name": "Pasta", "price": 200, "image": "pasta.jpeg"},
                    {"name": "Pizza", "price": 250, "image": "pizza.jpeg"},
                ]
            },
            "Burger House": {
                "items": [
                    {"name": "Burger", "price": 120, "image": "burger.jpeg"},
                    {"name": "Fries", "price": 80, "image": "fries.jpeg"},
                ]
            },
            "Asian Delight": {
                "items": [
                    {"name": "Noodles", "price": 150, "image": "noodles.jpeg"},
                    {"name": "Fried Rice", "price": 130, "image": "fried rice.jpeg"},
                ]
            },
            "Pizza Palace": {
                "items": [
                    {"name": "Margherita Pizza", "price": 220, "image": "pizza.jpeg"},
                    {"name": "Garlic Bread", "price": 90, "image": "garlic bread.jpeg"},
                ]
            }
        }
        
        # Create main panel
        self.main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(self.main_sizer)
        
        # Show login page first
        self.show_login_page()
        
        self.Centre()
        self.Show()
    
    def clear_panel(self):
        self.main_sizer.Clear(True)
        self.main_panel.Layout()
    
    def show_login_page(self):
        self.clear_panel()
        self.main_panel.SetBackgroundColour(wx.Colour(245, 245, 245))
        
        container = wx.BoxSizer(wx.VERTICAL)
        container.AddStretchSpacer(1)
        
        login_box = wx.BoxSizer(wx.VERTICAL)
        
        title = wx.StaticText(self.main_panel, label="🍔 FoodZone")
        title_font = wx.Font(32, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(wx.Colour(255, 87, 51))
        login_box.Add(title, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        subtitle = wx.StaticText(self.main_panel, label="Welcome back!")
        subtitle_font = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        subtitle.SetFont(subtitle_font)
        subtitle.SetForegroundColour(wx.Colour(100, 100, 100))
        login_box.Add(subtitle, 0, wx.ALIGN_CENTER | wx.BOTTOM, 30)
        
        email_label = wx.StaticText(self.main_panel, label="Email")
        email_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        login_box.Add(email_label, 0, wx.LEFT | wx.BOTTOM, 5)
        
        self.email_input = wx.TextCtrl(self.main_panel, size=(350, 40))
        self.email_input.SetHint("Enter your email")
        login_box.Add(self.email_input, 0, wx.EXPAND | wx.BOTTOM, 20)
        
        password_label = wx.StaticText(self.main_panel, label="Password")
        password_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        login_box.Add(password_label, 0, wx.LEFT | wx.BOTTOM, 5)
        
        self.password_input = wx.TextCtrl(self.main_panel, size=(350, 40), style=wx.TE_PASSWORD)
        self.password_input.SetHint("Enter your password")
        login_box.Add(self.password_input, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        info_text = wx.StaticText(self.main_panel, label="Demo: admin@food.com / admin123 or user@food.com / user123")
        info_text.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        info_text.SetForegroundColour(wx.Colour(120, 120, 120))
        login_box.Add(info_text, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        
        login_btn = wx.Button(self.main_panel, label="Login", size=(350, 45))
        login_btn.SetBackgroundColour(wx.Colour(255, 87, 51))
        login_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        login_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        login_btn.Bind(wx.EVT_BUTTON, self.on_login)
        login_box.Add(login_btn, 0, wx.EXPAND | wx.BOTTOM, 15)
        
        guest_btn = wx.Button(self.main_panel, label="Continue as Guest", size=(350, 40))
        guest_btn.SetBackgroundColour(wx.Colour(240, 240, 240))
        guest_btn.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        guest_btn.Bind(wx.EVT_BUTTON, self.on_guest_login)
        login_box.Add(guest_btn, 0, wx.EXPAND)
        
        container.Add(login_box, 0, wx.ALIGN_CENTER)
        container.AddStretchSpacer(1)
        
        self.main_sizer.Add(container, 1, wx.EXPAND | wx.ALL, 20)
        self.main_panel.Layout()
    
    def on_login(self, event):
        email = self.email_input.GetValue()
        password = self.password_input.GetValue()
        
        if email in self.users and self.users[email]["password"] == password:
            self.user_email = email
            self.is_admin = self.users[email]["is_admin"]
            
            if self.is_admin:
                self.show_admin_page()
            else:
                self.show_restaurant_selection()
        else:
            wx.MessageBox("Invalid email or password!", "Error", wx.OK | wx.ICON_ERROR)
    
    def on_guest_login(self, event):
        self.user_email = "guest@foodorder.com"
        self.is_admin = False
        self.show_restaurant_selection()
    
    def show_restaurant_selection(self):
        self.clear_panel()
        self.main_panel.SetBackgroundColour(wx.Colour(250, 250, 250))

        # Header
        header = wx.Panel(self.main_panel)
        header.SetBackgroundColour(wx.Colour(255, 87, 51))
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title = wx.StaticText(header, label="🍽️ Choose Your Restaurant")
        title.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour(255, 255, 255))
        header_sizer.Add(title, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)

        logout_btn = wx.Button(header, label="Logout", size=(100, 35))
        logout_btn.SetBackgroundColour(wx.Colour(255, 255, 255))
        logout_btn.SetForegroundColour(wx.Colour(255, 87, 51))
        logout_btn.Bind(wx.EVT_BUTTON, lambda e: self.show_login_page())
        header_sizer.Add(logout_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)

        header.SetSizer(header_sizer)
        self.main_sizer.Add(header, 0, wx.EXPAND)

        # Scrolled window for restaurants
        scroll = wx.ScrolledWindow(self.main_panel)
        scroll.SetScrollRate(10, 10)
        scroll.SetBackgroundColour(wx.Colour(250, 250, 250))
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)

        # Restaurant cards
        for restaurant_name in self.restaurants.keys():
            rest_panel = self.create_restaurant_card(scroll, restaurant_name)
            scroll_sizer.Add(rest_panel, 0, wx.EXPAND | wx.ALL, 15)

        scroll.SetSizer(scroll_sizer)
        self.main_sizer.Add(scroll, 1, wx.EXPAND)
        self.main_panel.Layout()
    
    def create_payment_method(self, parent, method):
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        panel.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        icon = wx.StaticText(panel, label=method["icon"])
        icon.SetFont(wx.Font(32, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        sizer.Add(icon, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)
        
        name = wx.StaticText(panel, label=method["name"])
        name.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(name, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)
        
        arrow = wx.StaticText(panel, label="→")
        arrow.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        arrow.SetForegroundColour(wx.Colour(200, 200, 200))
        sizer.Add(arrow, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)
        
        panel.SetSizer(sizer)
        
        panel.Bind(wx.EVT_LEFT_DOWN, lambda e, m=method: self.process_payment(m))
        icon.Bind(wx.EVT_LEFT_DOWN, lambda e, m=method: self.process_payment(m))
        name.Bind(wx.EVT_LEFT_DOWN, lambda e, m=method: self.process_payment(m))
        arrow.Bind(wx.EVT_LEFT_DOWN, lambda e, m=method: self.process_payment(m))
        
        return panel
    
    def process_payment(self, method):
        total = sum(item["price"] * item["quantity"] for item in self.cart)
        
        order = {
            "order_id": f"ORD{len(self.all_orders) + 1:04d}",
            "user": self.user_email,
            "restaurant": self.selected_restaurant,
            "items": self.cart.copy(),
            "total": total,
            "payment_method": method["name"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Confirmed"
        }
        self.all_orders.append(order)
        
        self.show_success_page(method, total)
    
    def show_success_page(self, payment_method, total):
        self.clear_panel()
        self.main_panel.SetBackgroundColour(wx.Colour(245, 245, 245))
        
        container = wx.BoxSizer(wx.VERTICAL)
        container.AddStretchSpacer(1)
        
        success_text = wx.StaticText(self.main_panel, label="✓")
        success_text.SetFont(wx.Font(100, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        success_text.SetForegroundColour(wx.Colour(76, 175, 80))
        container.Add(success_text, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        
        title = wx.StaticText(self.main_panel, label="Order Successful!")
        title.SetFont(wx.Font(28, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        container.Add(title, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        subtitle = wx.StaticText(self.main_panel, label="Your order has been placed successfully")
        subtitle.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        subtitle.SetForegroundColour(wx.Colour(100, 100, 100))
        container.Add(subtitle, 0, wx.ALIGN_CENTER | wx.BOTTOM, 30)
        
        details_panel = wx.Panel(self.main_panel)
        details_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        details_sizer = wx.BoxSizer(wx.VERTICAL)
        
        order_id_text = wx.StaticText(details_panel, label=f"Order ID: ORD{len(self.all_orders):04d}")
        order_id_text.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        details_sizer.Add(order_id_text, 0, wx.ALL, 10)
        
        payment_text = wx.StaticText(details_panel, label=f"Payment Method: {payment_method['name']}")
        payment_text.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        details_sizer.Add(payment_text, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        total_text = wx.StaticText(details_panel, label=f"Total Paid: ₹{total}")
        total_text.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        total_text.SetForegroundColour(wx.Colour(255, 87, 51))
        details_sizer.Add(total_text, 0, wx.ALL, 10)
        
        details_panel.SetSizer(details_sizer)
        container.Add(details_panel, 0, wx.ALIGN_CENTER | wx.BOTTOM, 40)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        home_btn = wx.Button(self.main_panel, label="Back to Restaurants", size=(180, 50))
        home_btn.SetBackgroundColour(wx.Colour(255, 87, 51))
        home_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        home_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        home_btn.Bind(wx.EVT_BUTTON, self.on_back_to_menu)
        btn_sizer.Add(home_btn, 0, wx.RIGHT, 10)
        
        container.Add(btn_sizer, 0, wx.ALIGN_CENTER)
        container.AddStretchSpacer(1)
        
        self.main_sizer.Add(container, 1, wx.EXPAND | wx.ALL, 20)
        self.main_panel.Layout()
    
    def on_back_to_menu(self, event):
        self.cart = []
        self.show_restaurant_selection()
    
    def show_admin_page(self):
        self.clear_panel()
        self.main_panel.SetBackgroundColour(wx.Colour(245, 245, 245))
        
        header = wx.Panel(self.main_panel)
        header.SetBackgroundColour(wx.Colour(63, 81, 181))
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        title = wx.StaticText(header, label="👨‍💼 Admin Dashboard")
        title.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour(255, 255, 255))
        header_sizer.Add(title, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        
        logout_btn = wx.Button(header, label="Logout", size=(100, 35))
        logout_btn.SetBackgroundColour(wx.Colour(255, 255, 255))
        logout_btn.SetForegroundColour(wx.Colour(63, 81, 181))
        logout_btn.Bind(wx.EVT_BUTTON, lambda e: self.show_login_page())
        header_sizer.Add(logout_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        
        header.SetSizer(header_sizer)
        self.main_sizer.Add(header, 0, wx.EXPAND)
        
        stats_panel = wx.Panel(self.main_panel)
        stats_panel.SetBackgroundColour(wx.Colour(245, 245, 245))
        stats_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        total_orders = len(self.all_orders)
        orders_card = self.create_stat_card(stats_panel, "📦", "Total Orders", str(total_orders), wx.Colour(33, 150, 243))
        stats_sizer.Add(orders_card, 1, wx.ALL, 10)
        
        total_revenue = sum(order["total"] for order in self.all_orders)
        revenue_card = self.create_stat_card(stats_panel, "💰", "Total Revenue", f"₹{total_revenue}", wx.Colour(76, 175, 80))
        stats_sizer.Add(revenue_card, 1, wx.ALL, 10)
        
        rest_count = len(self.restaurants)
        rest_card = self.create_stat_card(stats_panel, "🏪", "Restaurants", str(rest_count), wx.Colour(255, 152, 0))
        stats_sizer.Add(rest_card, 1, wx.ALL, 10)
        
        stats_panel.SetSizer(stats_sizer)
        self.main_sizer.Add(stats_panel, 0, wx.EXPAND | wx.ALL, 10)
        
        orders_header = wx.Panel(self.main_panel)
        orders_header.SetBackgroundColour(wx.Colour(255, 255, 255))
        orders_header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        orders_title = wx.StaticText(orders_header, label="Recent Orders")
        orders_title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        orders_header_sizer.Add(orders_title, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        
        orders_header.SetSizer(orders_header_sizer)
        self.main_sizer.Add(orders_header, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        if not self.all_orders:
            empty_panel = wx.Panel(self.main_panel)
            empty_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
            empty_sizer = wx.BoxSizer(wx.VERTICAL)
            
            empty_text = wx.StaticText(empty_panel, label="No orders yet")
            empty_text.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            empty_text.SetForegroundColour(wx.Colour(150, 150, 150))
            empty_sizer.Add(empty_text, 1, wx.ALIGN_CENTER | wx.ALL, 50)
            
            empty_panel.SetSizer(empty_sizer)
            self.main_sizer.Add(empty_panel, 1, wx.EXPAND | wx.ALL, 10)
        else:
            scroll = wx.ScrolledWindow(self.main_panel)
            scroll.SetScrollRate(10, 10)
            scroll.SetBackgroundColour(wx.Colour(245, 245, 245))
            scroll_sizer = wx.BoxSizer(wx.VERTICAL)
            
            for order in reversed(self.all_orders):
                order_panel = self.create_order_card(scroll, order)
                scroll_sizer.Add(order_panel, 0, wx.EXPAND | wx.ALL, 10)
            
            scroll.SetSizer(scroll_sizer)
            self.main_sizer.Add(scroll, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        self.main_panel.Layout()
    
    def create_stat_card(self, parent, icon, label, value, color):
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        icon_text = wx.StaticText(panel, label=icon)
        icon_text.SetFont(wx.Font(36, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        sizer.Add(icon_text, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        
        value_text = wx.StaticText(panel, label=value)
        value_text.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        value_text.SetForegroundColour(color)
        sizer.Add(value_text, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        
        label_text = wx.StaticText(panel, label=label)
        label_text.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        label_text.SetForegroundColour(wx.Colour(120, 120, 120))
        sizer.Add(label_text, 0, wx.ALIGN_CENTER | wx.ALL, 15)
        
        panel.SetSizer(sizer)
        return panel
    
    def create_order_card(self, parent, order):
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        order_id = wx.StaticText(panel, label=order["order_id"])
        order_id.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        header_sizer.Add(order_id, 0, wx.ALIGN_CENTER_VERTICAL)
        
        header_sizer.AddStretchSpacer(1)
        
        status = wx.StaticText(panel, label=order["status"])
        status.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        status.SetForegroundColour(wx.Colour(76, 175, 80))
        header_sizer.Add(status, 0, wx.ALIGN_CENTER_VERTICAL)
        
        main_sizer.Add(header_sizer, 0, wx.EXPAND | wx.ALL, 15)
        
        details_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        user_text = wx.StaticText(panel, label=f"User: {order['user']}")
        user_text.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        user_text.SetForegroundColour(wx.Colour(100, 100, 100))
        left_sizer.Add(user_text, 0, wx.BOTTOM, 5)
        
        rest_text = wx.StaticText(panel, label=f"Restaurant: {order['restaurant']}")
        rest_text.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        rest_text.SetForegroundColour(wx.Colour(100, 100, 100))
        left_sizer.Add(rest_text, 0, wx.BOTTOM, 5)
        
        items_text = wx.StaticText(panel, label=f"Items: {len(order['items'])}")
        items_text.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        items_text.SetForegroundColour(wx.Colour(100, 100, 100))
        left_sizer.Add(items_text, 0, wx.BOTTOM, 5)
        
        time_text = wx.StaticText(panel, label=f"Time: {order['timestamp']}")
        time_text.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        time_text.SetForegroundColour(wx.Colour(100, 100, 100))
        left_sizer.Add(time_text, 0)
        
        details_sizer.Add(left_sizer, 1)
        
        total_sizer = wx.BoxSizer(wx.VERTICAL)
        
        total_label = wx.StaticText(panel, label="Total")
        total_label.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        total_label.SetForegroundColour(wx.Colour(100, 100, 100))
        total_sizer.Add(total_label, 0, wx.ALIGN_RIGHT | wx.BOTTOM, 5)
        
        total_value = wx.StaticText(panel, label=f"₹{order['total']}")
        total_value.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        total_value.SetForegroundColour(wx.Colour(63, 81, 181))
        total_sizer.Add(total_value, 0, wx.ALIGN_RIGHT)
        
        payment_method = wx.StaticText(panel, label=order['payment_method'])
        payment_method.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        payment_method.SetForegroundColour(wx.Colour(120, 120, 120))
        total_sizer.Add(payment_method, 0, wx.ALIGN_RIGHT | wx.TOP, 5)
        
        details_sizer.Add(total_sizer, 0)
        
        main_sizer.Add(details_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        
        panel.SetSizer(main_sizer)
        return panel


        
        scroll = wx.ScrolledWindow(self.main_panel)
        scroll.SetScrollRate(10, 10)
        scroll.SetBackgroundColour(wx.Colour(250, 250, 250))
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        
        for restaurant_name in self.restaurants.keys():
            rest_panel = self.create_restaurant_card(scroll, restaurant_name)
            scroll_sizer.Add(rest_panel, 0, wx.EXPAND | wx.ALL, 15)
        
        scroll.SetSizer(scroll_sizer)
        self.main_sizer.Add(scroll, 1, wx.EXPAND)
        self.main_panel.Layout()

    def create_restaurant_card(self, parent, restaurant_name):
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        icon_panel = wx.Panel(panel, size=(80, 80))
        icon_panel.SetBackgroundColour(wx.Colour(255, 237, 230))
        icon_sizer = wx.BoxSizer(wx.VERTICAL)
        icon_text = wx.StaticText(icon_panel, label="🍴")
        icon_text.SetFont(wx.Font(36, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        icon_sizer.Add(icon_text, 1, wx.ALIGN_CENTER)
        icon_panel.SetSizer(icon_sizer)
        sizer.Add(icon_panel, 0, wx.ALL, 15)
        
        info_sizer = wx.BoxSizer(wx.VERTICAL)
        
        name = wx.StaticText(panel, label=restaurant_name)
        name.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        info_sizer.Add(name, 0, wx.BOTTOM, 5)
        
        items_count = len(self.restaurants[restaurant_name]["items"])
        desc = wx.StaticText(panel, label=f"{items_count} items available")
        desc.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        desc.SetForegroundColour(wx.Colour(120, 120, 120))
        info_sizer.Add(desc, 0)
        
        sizer.Add(info_sizer, 1, wx.ALIGN_CENTER_VERTICAL)
        
        browse_btn = wx.Button(panel, label="Browse Menu →", size=(150, 40))
        browse_btn.SetBackgroundColour(wx.Colour(255, 87, 51))
        browse_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        browse_btn.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        browse_btn.Bind(wx.EVT_BUTTON, lambda e, r=restaurant_name: self.select_restaurant(r))
        sizer.Add(browse_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        
        panel.SetSizer(sizer)
        return panel
    
    def select_restaurant(self, restaurant_name):
        self.selected_restaurant = restaurant_name
        self.show_menu_page()
    
    def show_menu_page(self):
        self.clear_panel()
        self.main_panel.SetBackgroundColour(wx.Colour(250, 250, 250))
        
        header = wx.Panel(self.main_panel)
        header.SetBackgroundColour(wx.Colour(255, 87, 51))
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        back_btn = wx.Button(header, label="← Restaurants", size=(140, 35))
        back_btn.SetBackgroundColour(wx.Colour(255, 255, 255))
        back_btn.SetForegroundColour(wx.Colour(255, 87, 51))
        back_btn.Bind(wx.EVT_BUTTON, lambda e: self.show_restaurant_selection())
        header_sizer.Add(back_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        
        title = wx.StaticText(header, label=f"🍔 {self.selected_restaurant}")
        title.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour(255, 255, 255))
        header_sizer.Add(title, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        
        cart_btn = wx.Button(header, label=f"🛒 Cart ({len(self.cart)})", size=(120, 35))
        cart_btn.SetBackgroundColour(wx.Colour(255, 255, 255))
        cart_btn.SetForegroundColour(wx.Colour(255, 87, 51))
        cart_btn.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        cart_btn.Bind(wx.EVT_BUTTON, lambda e: self.show_cart_page())
        header_sizer.Add(cart_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        
        header.SetSizer(header_sizer)
        self.main_sizer.Add(header, 0, wx.EXPAND)
        
        scroll = wx.ScrolledWindow(self.main_panel)
        scroll.SetScrollRate(10, 10)
        scroll.SetBackgroundColour(wx.Colour(250, 250, 250))
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        
        items = self.restaurants[self.selected_restaurant]["items"]
        grid = wx.GridSizer(2, 2, 20, 20)
        
        for item in items:
            item_panel = self.create_menu_item(scroll, item)
            grid.Add(item_panel, 0, wx.EXPAND)
        
        scroll_sizer.Add(grid, 0, wx.ALL | wx.EXPAND, 30)
        scroll.SetSizer(scroll_sizer)
        
        self.main_sizer.Add(scroll, 1, wx.EXPAND)
        self.main_panel.Layout()
    
    def create_menu_item(self, parent, item):
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        img_panel = wx.Panel(panel, size=(-1, 200))
        img_panel.SetBackgroundColour(wx.Colour(230, 230, 230))
        img_sizer = wx.BoxSizer(wx.VERTICAL)
        
        image_path = os.path.join("images", item["image"])
        if os.path.exists(image_path):
            try:
                img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
                img = img.Scale(250, 200, wx.IMAGE_QUALITY_HIGH)
                bitmap = wx.StaticBitmap(img_panel, bitmap=wx.Bitmap(img))
                img_sizer.Add(bitmap, 1, wx.EXPAND)
            except:
                img_text = wx.StaticText(img_panel, label="🍽️")
                img_text.SetFont(wx.Font(48, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                img_sizer.Add(img_text, 1, wx.ALIGN_CENTER)
        else:
            img_text = wx.StaticText(img_panel, label="🍽️")
            img_text.SetFont(wx.Font(48, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            img_sizer.Add(img_text, 1, wx.ALIGN_CENTER)
        
        img_panel.SetSizer(img_sizer)
        sizer.Add(img_panel, 0, wx.EXPAND)
        
        details_sizer = wx.BoxSizer(wx.VERTICAL)
        
        name = wx.StaticText(panel, label=item["name"])
        name.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        details_sizer.Add(name, 0, wx.ALL, 10)
        
        price = wx.StaticText(panel, label=f"₹{item['price']}")
        price.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        price.SetForegroundColour(wx.Colour(255, 87, 51))
        details_sizer.Add(price, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        add_btn = wx.Button(panel, label="Add to Cart", size=(-1, 40))
        add_btn.SetBackgroundColour(wx.Colour(255, 87, 51))
        add_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        add_btn.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        add_btn.Bind(wx.EVT_BUTTON, lambda e, i=item: self.add_to_cart(i))
        details_sizer.Add(add_btn, 0, wx.EXPAND | wx.ALL, 10)
        
        sizer.Add(details_sizer, 0, wx.EXPAND)
        panel.SetSizer(sizer)
        
        return panel
    
    def add_to_cart(self, item):
        for cart_item in self.cart:
            if cart_item["name"] == item["name"]:
                cart_item["quantity"] += 1
                wx.MessageBox(f"Added {item['name']} to cart!", "Success", wx.OK | wx.ICON_INFORMATION)
                return
        
        self.cart.append({**item, "quantity": 1})
        wx.MessageBox(f"Added {item['name']} to cart!", "Success", wx.OK | wx.ICON_INFORMATION)
    
    def show_cart_page(self):
        self.clear_panel()
        self.main_panel.SetBackgroundColour(wx.Colour(245, 245, 245))
        
        header = wx.Panel(self.main_panel)
        header.SetBackgroundColour(wx.Colour(255, 255, 255))
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        back_btn = wx.Button(header, label="← Back", size=(100, 35))
        back_btn.Bind(wx.EVT_BUTTON, lambda e: self.show_menu_page())
        header_sizer.Add(back_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        
        title = wx.StaticText(header, label="🛒 Your Cart")
        title.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        header_sizer.Add(title, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)
        
        header.SetSizer(header_sizer)
        self.main_sizer.Add(header, 0, wx.EXPAND)
        
        if not self.cart:
            empty_sizer = wx.BoxSizer(wx.VERTICAL)
            empty_sizer.AddStretchSpacer(1)
            
            empty_text = wx.StaticText(self.main_panel, label="Your cart is empty!")
            empty_text.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            empty_text.SetForegroundColour(wx.Colour(150, 150, 150))
            empty_sizer.Add(empty_text, 0, wx.ALIGN_CENTER)
            
            empty_sizer.AddStretchSpacer(1)
            self.main_sizer.Add(empty_sizer, 1, wx.EXPAND)
        else:
            scroll = wx.ScrolledWindow(self.main_panel)
            scroll.SetScrollRate(10, 10)
            scroll.SetBackgroundColour(wx.Colour(245, 245, 245))
            scroll_sizer = wx.BoxSizer(wx.VERTICAL)
            
            for item in self.cart:
                item_panel = self.create_cart_item(scroll, item)
                scroll_sizer.Add(item_panel, 0, wx.EXPAND | wx.ALL, 10)
            
            scroll.SetSizer(scroll_sizer)
            self.main_sizer.Add(scroll, 1, wx.EXPAND)
            
            footer = wx.Panel(self.main_panel)
            footer.SetBackgroundColour(wx.Colour(255, 255, 255))
            footer_sizer = wx.BoxSizer(wx.HORIZONTAL)
            
            total = sum(item["price"] * item["quantity"] for item in self.cart)
            total_text = wx.StaticText(footer, label=f"Total: ₹{total}")
            total_text.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            footer_sizer.Add(total_text, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)
            
            checkout_btn = wx.Button(footer, label="Proceed to Payment", size=(200, 50))
            checkout_btn.SetBackgroundColour(wx.Colour(76, 175, 80))
            checkout_btn.SetForegroundColour(wx.Colour(255, 255, 255))
            checkout_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            checkout_btn.Bind(wx.EVT_BUTTON, lambda e: self.show_payment_page())
            footer_sizer.Add(checkout_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)
            
            footer.SetSizer(footer_sizer)
            self.main_sizer.Add(footer, 0, wx.EXPAND)
        
        self.main_panel.Layout()
    
    def create_cart_item(self, parent, item):
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        img_panel = wx.Panel(panel, size=(100, 100))
        img_panel.SetBackgroundColour(wx.Colour(230, 230, 230))
        img_sizer = wx.BoxSizer(wx.VERTICAL)
        
        image_path = os.path.join("images", item["image"])
        if os.path.exists(image_path):
            try:
                img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
                img = img.Scale(100, 100, wx.IMAGE_QUALITY_HIGH)
                bitmap = wx.StaticBitmap(img_panel, bitmap=wx.Bitmap(img))
                img_sizer.Add(bitmap, 1, wx.EXPAND)
            except:
                img_text = wx.StaticText(img_panel, label="🍽️")
                img_text.SetFont(wx.Font(32, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                img_sizer.Add(img_text, 1, wx.ALIGN_CENTER)
        else:
            img_text = wx.StaticText(img_panel, label="🍽️")
            img_text.SetFont(wx.Font(32, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            img_sizer.Add(img_text, 1, wx.ALIGN_CENTER)
        
        img_panel.SetSizer(img_sizer)
        sizer.Add(img_panel, 0, wx.ALL, 10)
        
        details_sizer = wx.BoxSizer(wx.VERTICAL)
        
        name = wx.StaticText(panel, label=item["name"])
        name.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        details_sizer.Add(name, 0, wx.BOTTOM, 5)
        
        price = wx.StaticText(panel, label=f"₹{item['price']}")
        price.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        price.SetForegroundColour(wx.Colour(100, 100, 100))
        details_sizer.Add(price, 0)
        
        sizer.Add(details_sizer, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        
        qty_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        minus_btn = wx.Button(panel, label="-", size=(40, 40))
        minus_btn.Bind(wx.EVT_BUTTON, lambda e, i=item: self.update_quantity(i, -1))
        qty_sizer.Add(minus_btn, 0, wx.ALL, 5)
        
        qty_text = wx.StaticText(panel, label=str(item["quantity"]))
        qty_text.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        qty_sizer.Add(qty_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 15)
        
        plus_btn = wx.Button(panel, label="+", size=(40, 40))
        plus_btn.Bind(wx.EVT_BUTTON, lambda e, i=item: self.update_quantity(i, 1))
        qty_sizer.Add(plus_btn, 0, wx.ALL, 5)
        
        sizer.Add(qty_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        
        remove_btn = wx.Button(panel, label="Remove", size=(100, 40))
        remove_btn.SetBackgroundColour(wx.Colour(255, 87, 51))
        remove_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        remove_btn.Bind(wx.EVT_BUTTON, lambda e, i=item: self.remove_from_cart(i))
        sizer.Add(remove_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        
        panel.SetSizer(sizer)
        return panel
    
    def update_quantity(self, item, change):
        for cart_item in self.cart:
            if cart_item["name"] == item["name"]:
                cart_item["quantity"] += change
                if cart_item["quantity"] <= 0:
                    self.cart.remove(cart_item)
                self.show_cart_page()
                return
    
    def remove_from_cart(self, item):
        self.cart = [i for i in self.cart if i["name"] != item["name"]]
        self.show_cart_page()
    
    def show_payment_page(self):
        self.clear_panel()
        self.main_panel.SetBackgroundColour(wx.Colour(245, 245, 245))

        # Header
        header = wx.Panel(self.main_panel)
        header.SetBackgroundColour(wx.Colour(255, 255, 255))
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)

        back_btn = wx.Button(header, label="← Back", size=(100, 35))
        back_btn.Bind(wx.EVT_BUTTON, lambda e: self.show_cart_page())
        header_sizer.Add(back_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)

        title = wx.StaticText(header, label="💳 Select Payment Method")
        title.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        header_sizer.Add(title, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)

        header.SetSizer(header_sizer)
        self.main_sizer.Add(header, 0, wx.EXPAND)

        # Container for payment options
        container = wx.BoxSizer(wx.VERTICAL)
        container.AddSpacer(30)

        total = sum(item["price"] * item["quantity"] for item in self.cart)
        total_panel = wx.Panel(self.main_panel)
        total_panel.SetBackgroundColour(wx.Colour(255, 245, 235))
        total_sizer = wx.BoxSizer(wx.VERTICAL)

        total_text = wx.StaticText(total_panel, label=f"Amount to Pay: ₹{total}")
        total_text.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        total_text.SetForegroundColour(wx.Colour(255, 87, 51))
        total_sizer.Add(total_text, 0, wx.ALL | wx.ALIGN_CENTER, 20)

        total_panel.SetSizer(total_sizer)
        container.Add(total_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 50)

        container.AddSpacer(20)

        payment_methods = [
            {"name": "Google Pay", "icon": "💳", "id": "gpay"},
            {"name": "PhonePe", "icon": "📱", "id": "phonepe"},
            {"name": "Paytm", "icon": "💰", "id": "paytm"}
        ]

        for method in payment_methods:
            method_panel = self.create_payment_method(self.main_panel, method)
            container.Add(method_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 50)

        self.main_sizer.Add(container, 1, wx.EXPAND)
        self.main_panel.Layout()


if __name__ == "__main__":
    app = wx.App(False)
    frame = FoodOrderApp()
    app.MainLoop()