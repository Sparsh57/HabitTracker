import rumps

class TodoBarApp(rumps.App):
    def __init__(self):
        super(TodoBarApp, self).__init__("ToDo")
        self.menu = ["Task 1", "Task 2", "Update GitHub Status"]

    @rumps.clicked("Update GitHub Status")
    def update_status(self, _):
        # Code to check GitHub and update menu items
        pass

if __name__ == "__main__":
    TodoBarApp().run()