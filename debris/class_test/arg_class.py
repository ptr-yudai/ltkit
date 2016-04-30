#
# class test
#
class Parent:
    def __init__(self):
        self.child = Parent.Child()
        self.child.func(self)
        print(self.parent_var)
        print(self.child.child_var)
        return

    class Child:
        def func(self, parent):
            parent.parent_var = 3.14
            parent.child.child_var = 2.71
            print(parent.child.child_var)
            print(self.child_var)
            return

Parent()
