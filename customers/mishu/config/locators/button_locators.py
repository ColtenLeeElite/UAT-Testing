from playwright.async_api import Page
from wrapper import LocatorDescriptor



class Edit_Agent():
#--------pin agents------------------
    button_pin_agent = LocatorDescriptor()
    'Leon "Pin agent in the front page "'
#--------Documents----------------------------------------------------
    button_add_URL= LocatorDescriptor()
    'Leon "button click on add URL in edit agent"'
    
#----------integration -----------
    button_enable_web_widget = LocatorDescriptor()
    'Leon "Enable web widget in integration"'
    button_widget_drop_down = LocatorDescriptor()
    'Leon "Chat Widget Language drop down"'

    button_add_escalation = LocatorDescriptor()
    'Leon "Add escalation flow"'

    button_create_link_script = LocatorDescriptor()
    'Leon "Create link to Copy script to Install"'

    button_add_new_field = LocatorDescriptor()
    'Leon  "Add new fields in contact form"'
#----------web widget -----------
    

    def __init__(self, page: Page):
        super().__init__(page)
        self.button_pin_agent = page.locator("//input[@id='continue']")
        self.button_add_URL = page.locator("//button[@data-test='cancel']")
        self.button_enable_web_widget = page.locator("//input[@data-test='firstName']")
        self.button_widget_drop_down = page.locator("//input[@data-test='lastName']")
        self.button_add_escalation = page.locator("//input[@data-test='postalCode']")
        self.button_create_link_script = page.locator("//button[@data-test='finish']")
        self.button_add_new_field = page.locator("//button[@data-test='back-to-products']")
