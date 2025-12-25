# main.py — Version 2.0, dashboard layout, Tkinter only
import tkinter as tk
from tkinter import ttk, messagebox

from utils import (
    load_data,
    add_transaction,
    delete_transaction,
    summary_totals,
    summary_by_category,
)
from charts import chart_category_distribution, chart_category_bars, embed_figure_tk

FONT_TITLE = ("Segoe UI", 12, "bold")
FONT_NORMAL = ("Segoe UI", 10)

# Categories and subcategories based on your list
CATEGORIES = {
    "Housing": [
        "Rent or Mortgage",
        "Property Taxes",
        "Homeowners or Renters Insurance",
        "HOA Fees",
        "Home Maintenance & Repairs",
        "Utilities",
    ],
    "Transportation": [
        "Car Payment",
        "Fuel/Gas",
        "Auto Insurance",
        "Maintenance & Repairs",
        "Registration & Inspection",
        "Public Transportation / Rideshare",
    ],
    "Food": [
        "Groceries",
        "Dining Out / Takeout",
        "Coffee / Snacks",
    ],
    "Childcare & Kids": [
        "Childcare / Babysitting",
        "School Tuition / Fees",
        "School Supplies",
        "Kids' Activities / Sports",
        "Clothing & Shoes",
        "Toys & Games",
    ],
    "Health & Insurance": [
        "Health Insurance",
        "Medical Bills & Copays",
        "Dental & Vision Care",
        "Medications",
        "Life Insurance",
    ],
    "Debt Payments": [
        "Credit Card Payments",
        "Student Loans",
        "Personal Loans",
        "Medical Debt",
    ],
    "Personal & Lifestyle": [
        "Clothing & Accessories",
        "Haircuts & Personal Care",
        "Subscriptions",
        "Gym or Fitness Membership",
        "Hobbies",
    ],
    "Technology & Services": [
        "Internet",
        "Cell Phone",
        "Software / App Subscriptions",
        "Streaming Services",
    ],
    "Gifts & Holidays": [
        "Birthday Gifts",
        "Holiday Gifts",
        "Decorations",
        "Holiday Meals / Events",
    ],
    "Education & Learning": [
        "Tuition",
        "Books & Supplies",
        "Courses / Certifications",
        "Kids' Educational Materials",
    ],
    "Savings & Investments": [
        "Emergency Fund",
        "Retirement Contributions",
        "Vacation Savings",
        "Sinking Funds",
        "Investments",
    ],
    "Pets": [
        "Food",
        "Vet Bills",
        "Pet Insurance",
        "Grooming",
        "Supplies & Toys",
    ],
    "Giving": [
        "Tithing / Church Giving",
        "Charitable Donations",
        "Fundraisers",
    ],
    "Miscellaneous": [
        "Bank Fees",
        "Postage",
        "Parking / Tolls",
        "Unexpected Expenses",
    ],
}


def create_interface():
    root = tk.Tk()
    root.title("Personal Budget Manager — Version 2.0")
    root.geometry("1200x800")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=24, font=FONT_NORMAL)
    style.configure("Treeview.Heading", font=FONT_TITLE)

    # Layout grid
    root.columnconfigure(0, weight=3)
    root.columnconfigure(1, weight=2)
    root.rowconfigure(2, weight=1)

    # ------------------------------
    # HEADER
    # ------------------------------
    header = ttk.Frame(root, padding=10)
    header.grid(row=0, column=0, columnspan=2, sticky="ew")

    title_label = ttk.Label(header, text="Budget Personal", font=("Segoe UI", 16, "bold"))
    title_label.pack(anchor="w")

    # ------------------------------
    # TOP SUMMARY (LEFT SIDE)
    # ------------------------------
    summary_frame = ttk.Frame(root, padding=10)
    summary_frame.grid(row=1, column=0, sticky="ew")
    for i in range(2):
        summary_frame.columnconfigure(i, weight=1)

    lbl_total_spent = ttk.Label(summary_frame, text="TOTAL SPENT: $0.00", font=FONT_TITLE)
    lbl_total_spent.grid(row=0, column=0, sticky="w", padx=5)

    # You can add more summary labels here later if needed.

    # ------------------------------
    # CHARTS AREA (LEFT SIDE)
    # ------------------------------
    charts_frame = ttk.Frame(root, padding=10)
    charts_frame.grid(row=2, column=0, sticky="nsew")
    charts_frame.columnconfigure(0, weight=1)
    charts_frame.columnconfigure(1, weight=1)
    charts_frame.rowconfigure(0, weight=1)

    chart_frame1 = ttk.LabelFrame(charts_frame, text="Category distribution", padding=10)
    chart_frame1.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

    chart_frame2 = ttk.LabelFrame(charts_frame, text="Total by category", padding=10)
    chart_frame2.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

    # ------------------------------
    # TRANSACTIONS TABLE (BOTTOM LEFT)
    # ------------------------------
    table_frame = ttk.LabelFrame(root, text="Transactions", padding=10)
    table_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    cols = ("#", "Date", "Category", "Subcategory", "Amount")
    tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor="center")
    tree.grid(row=0, column=0, sticky="nsew")

    scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scroll.set)
    scroll.grid(row=0, column=1, sticky="ns")

    btn_delete = ttk.Button(table_frame, text="Delete selected")
    btn_delete.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

    # ------------------------------
    # INPUT PANEL (RIGHT SIDE)
    # ------------------------------
    input_frame = ttk.LabelFrame(root, text="Add transaction", padding=10)
    input_frame.grid(row=1, column=1, rowspan=3, sticky="nsew", padx=(0, 10), pady=(10, 10))
    for i in range(2):
        input_frame.columnconfigure(i, weight=1)

    # Date
    ttk.Label(input_frame, text="Date (YYYY-MM-DD):", font=FONT_NORMAL).grid(
        row=0, column=0, sticky="w", pady=5
    )
    entry_date = ttk.Entry(input_frame)
    entry_date.grid(row=0, column=1, sticky="ew", pady=5)

    # Category
    ttk.Label(input_frame, text="Category:", font=FONT_NORMAL).grid(
        row=1, column=0, sticky="w", pady=5
    )
    cb_category = ttk.Combobox(
        input_frame, values=list(CATEGORIES.keys()), state="readonly"
    )
    cb_category.grid(row=1, column=1, sticky="ew", pady=5)

    # Subcategory
    ttk.Label(input_frame, text="Subcategory:", font=FONT_NORMAL).grid(
        row=2, column=0, sticky="w", pady=5
    )
    cb_subcategory = ttk.Combobox(input_frame, values=[], state="readonly")
    cb_subcategory.grid(row=2, column=1, sticky="ew", pady=5)

    # Amount
    ttk.Label(input_frame, text="Amount:", font=FONT_NORMAL).grid(
        row=3, column=0, sticky="w", pady=5
    )
    entry_amount = ttk.Entry(input_frame)
    entry_amount.grid(row=3, column=1, sticky="ew", pady=5)

    # Add button
    btn_add = ttk.Button(input_frame, text="Add transaction")
    btn_add.grid(row=4, column=0, columnspan=2, sticky="ew", pady=15)

    # ------------------------------
    # LOGIC FUNCTIONS
    # ------------------------------
    def update_subcategories(*args):
        """
        Updates the subcategory combobox when category changes.
        """
        cat = cb_category.get()
        options = CATEGORIES.get(cat, [])
        cb_subcategory["values"] = options
        if options:
            cb_subcategory.set(options[0])
        else:
            cb_subcategory.set("")

    def update_summary():
        totals = summary_totals()
        lbl_total_spent.config(text=f"TOTAL SPENT: ${totals['total_spent']:.2f}")

    def update_table():
        df = load_data()
        for row in tree.get_children():
            tree.delete(row)
        for i, r in df.reset_index().iterrows():
            tree.insert(
                "",
                "end",
                iid=str(i),
                values=(
                    i + 1,
                    r["Date"],
                    r["Category"],
                    r["Subcategory"],
                    f"{r['Amount']:.2f}",
                ),
            )

    def update_charts():
        for f in (chart_frame1, chart_frame2):
            for child in f.winfo_children():
                child.destroy()

        df_summary = summary_by_category()
        fig1 = chart_category_distribution(df_summary)
        fig2 = chart_category_bars(df_summary)

        embed_figure_tk(fig1, chart_frame1)
        embed_figure_tk(fig2, chart_frame2)

    # ------------------------------
    # BUTTON ACTIONS
    # ------------------------------
    def add_action():
        date = entry_date.get().strip()
        category = cb_category.get().strip()
        subcategory = cb_subcategory.get().strip()
        amount_text = entry_amount.get().strip()

        if not (date and category and subcategory and amount_text):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return

        add_transaction(date, category, subcategory, amount)

        entry_amount.delete(0, tk.END)

        update_table()
        update_summary()
        update_charts()

    def delete_action():
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Please select a row to delete.")
            return
        iid = sel[0]
        idx = int(iid)
        delete_transaction(idx)

        update_table()
        update_summary()
        update_charts()

    # Bind logic
    cb_category.bind("<<ComboboxSelected>>", update_subcategories)
    btn_add.config(command=add_action)
    btn_delete.config(command=delete_action)

    # ------------------------------
    # INITIALIZATION
    # ------------------------------
    update_table()
    update_summary()
    update_charts()

    root.mainloop()


if __name__ == "__main__":
    create_interface()
