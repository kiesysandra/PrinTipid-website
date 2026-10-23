from pyscript import document, when

PRICES = {
    "Black-and-white printing": 2.00,
    "Colored printing": 5.00,
    "Photocopy": 1.00
}
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = (".pdf", ".doc", ".docx", ".png", ".jpg", ".jpeg")

def value(element_id):
    element = document.getElementById(element_id)
    return element.value.strip() if element and element.value else ""

def checked_value(name, default=""):
    items = document.querySelectorAll(f'input[name="{name}"]')
    for item in items:
        if item.checked:
            return item.value
    return default

def selected_service():
    return checked_value("service", "Black-and-white printing")

def money(amount):
    return f"₱{amount:,.2f}"

def get_quote(show_errors=False):
    try:
        pages = int(value("pages"))
        copies = int(value("copies"))
    except ValueError:
        if show_errors:
            message("Pages and copies must be whole numbers.", True)
        return None
    if pages < 1 or copies < 1:
        if show_errors:
            message("Pages and copies must each be at least 1.", True)
        return None
    service = selected_service()
    rate = PRICES.get(service)
    if rate is None:
        if show_errors:
            message("Please choose a valid printing service.", True)
        return None
    staple_fee = 3.00 if document.getElementById("stapling").checked else 0.00
    subtotal = pages * copies * rate
    return {
        "pages": pages, "copies": copies, "service": service,
        "rate": rate, "staple_fee": staple_fee, "total": subtotal + staple_fee,
        "paper": value("paper-size"), "delivery": checked_value("delivery", "Campus pickup")
    }

def message(text, error=False):
    box = document.getElementById("form-message")
    box.textContent = text
    box.style.color = "#c33b3b" if error else "#07865f"

def update_customer_fields():
    customer_type = checked_value("customer-type", "Student")
    is_student = customer_type == "Student"
    document.getElementById("student-fields").hidden = not is_student
    document.getElementById("staff-fields").hidden = is_student

def update_quote():
    quote = get_quote()
    if quote is None:
        return
    short_service = {
        "Black-and-white printing": "Black & white",
        "Colored printing": "Color printing",
        "Photocopy": "Photocopy"
    }[quote["service"]]
    document.getElementById("live-total").textContent = money(quote["total"])
    document.getElementById("price-equation").textContent = (
        f'{quote["pages"]} page(s) × {quote["copies"]} copy/copies × '
        f'{money(quote["rate"])}' +
        (f' + {money(quote["staple_fee"])} stapling' if quote["staple_fee"] else "")
    )
    document.getElementById("live-service").textContent = short_service
    document.getElementById("live-quantity").textContent = f'{quote["pages"]} page(s) / {quote["copies"]} cop(y/ies)'
    document.getElementById("live-paper").textContent = quote["paper"]
    document.getElementById("live-finishing").textContent = "Stapling" if quote["staple_fee"] else "None"
    document.getElementById("live-delivery").textContent = quote["delivery"]

def validate_request():
    name = value("full-name")
    if not name:
        return None, "Please enter the customer's full name."
    customer_type = checked_value("customer-type", "Student")
    course = value("course")
    department = value("department")
    if customer_type == "Student" and not course:
        return None, "Please enter the student's course, year, and section."
    if customer_type != "Student" and not department:
        return None, "Please enter the department or office."
    quote = get_quote(show_errors=True)
    if quote is None:
        return None, "Please check the pages and copies fields."
    file_input = document.getElementById("document-file")
    files = file_input.files
    filename = "No file selected"
    if files.length > 0:
        file = files.item(0)
        filename = file.name
        lower_name = filename.lower()
        if not lower_name.endswith(ALLOWED_EXTENSIONS):
            return None, "File type not supported. Please select PDF, DOC, DOCX, PNG, or JPG."
        if file.size > MAX_FILE_SIZE:
            return None, "The selected file is larger than 10 MB."
    return {
        "name": name, "customer_type": customer_type,
        "customer_id": value("customer-id") or "Not provided",
        "course": course, "department": department,
        "building": value("building") or "Not provided",
        "contact": value("contact") or "Not provided",
        "filename": filename, "instructions": value("instructions") or "None",
        "quote": quote
    }, None

def show_review(details):
    q = details["quote"]
    summary = [
        f'Customer: {details["name"]}',
        f'Type: {details["customer_type"]}',
        f'ID: {details["customer_id"]}'
    ]
    if details["customer_type"] == "Student":
        summary.append(f'Course / year / section: {details["course"]}')
    else:
        summary.append(f'Department / office: {details["department"]}')
    summary += [
        f'Room / building: {details["building"]}',
        f'Contact: {details["contact"]}',
        f'File name: {details["filename"]}',
        f'Service: {q["service"]}',
        f'Pages: {q["pages"]}',
        f'Copies: {q["copies"]}',
        f'Paper size: {q["paper"]}',
        f'Stapling: {"Yes" if q["staple_fee"] else "No"}',
        f'Claiming preference: {q["delivery"]}',
        f'Special instructions: {details["instructions"]}',
        f'Estimated total: {money(q["total"])}',
        '',
        'Status: Pending review (demo only)'
    ]
    document.getElementById("summary-text").textContent = "\n".join(summary)
    document.getElementById("final-summary").hidden = False
    document.querySelector(".status-pill").textContent = "Review ready"
    message("Request summary prepared. This is a demo only; no order has been sent or saved.")

@when("change", 'input[name="customer-type"]')
def customer_changed(event):
    update_customer_fields()

@when("input", "#pages")
def pages_changed(event):
    update_quote()

@when("input", "#copies")
def copies_changed(event):
    update_quote()

@when("change", 'input[name="service"]')
def service_changed(event):
    update_quote()

@when("change", "#paper-size")
def paper_changed(event):
    update_quote()

@when("change", "#stapling")
def stapling_changed(event):
    update_quote()

@when("change", 'input[name="delivery"]')
def delivery_changed(event):
    update_quote()

@when("change", "#document-file")
def file_changed(event):
    files = document.getElementById("document-file").files
    if files.length > 0:
        file = files.item(0)
        document.getElementById("file-name").textContent = f"{file.name} ({file.size // 1024} KB)"
    else:
        document.getElementById("file-name").textContent = "No file selected"

@when("click", "#remove-file")
def remove_file(event):
    document.getElementById("document-file").value = ""
    document.getElementById("file-name").textContent = "No file selected"

@when("click", "#calculate-btn")
def calculate_clicked(event):
    quote = get_quote(show_errors=True)
    if quote:
        update_quote()
        message(f'Your estimated total is {money(quote["total"])}. Review all details before submitting.')

@when("click", "#summary-submit")
def summary_clicked(event):
    details, error = validate_request()
    if error:
        message(error, True)
        return
    show_review(details)

@when("submit", "#order-form")
def form_submitted(event):
    event.preventDefault()
    details, error = validate_request()
    if error:
        message(error, True)
        return
    show_review(details)

@when("reset", "#order-form")
def form_reset(event):
    document.getElementById("final-summary").hidden = True
    document.getElementById("summary-text").textContent = ""
    document.getElementById("file-name").textContent = "No file selected"
    document.querySelector(".status-pill").textContent = "Not submitted"
    message("Form cleared.")
    update_customer_fields()
    update_quote()

update_customer_fields()
update_quote()
