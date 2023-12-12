class SnailFish:
    def __init__(self):
        self.left = self.right = self.value = self.parent = self.depth = None

    def clone(self):
        cloned = SnailFish()
        if self.left:
            cloned.left = self.left.clone()
            cloned.left.parent = cloned
        if self.right:
            cloned.right = self.right.clone()
            cloned.right.parent = cloned
        cloned.value = self.value
        cloned.depth = self.depth
        return cloned

    def from_snails(self, left, right):
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
        self.depth = 0
        self.left.inc_depth()
        self.right.inc_depth()

    def inc_depth(self):
        self.depth += 1
        if self.left:
            self.left.inc_depth()
            self.right.inc_depth()

    def from_str(self, str_value, depth=0, parent=None):
        self.value = None
        self.left = self.right = None
        self.depth = depth
        self.parent = parent
        if str_value[0].isdigit():
            self.value = int(str_value)
        else:
            str_value = str_value[1:-1]
            b = 0
            for i, a in enumerate(str_value):
                b += a == "["
                b -= a == "]"
                if b == 0 and a == ",":
                    break
            self.left = SnailFish()
            self.left.from_str(str_value[:i], depth + 1, self)
            self.right = SnailFish()
            self.right.from_str(str_value[i + 1 :], depth + 1, self)
        return self

    def reduce_explosion(self):
        if self.depth > 3 and self.left and self.right:
            to_left = self.left.value
            to_right = self.right.value
            self.value = 0
            self.right = self.left = None
            prev = self
            this = self.parent
            while this and this.left == prev:
                prev = this
                this = this.parent
            if this:
                this = this.left
                while this.right:
                    this = this.right
                this.value += to_left
            prev = self
            this = self.parent
            while this and this.right == prev:
                prev = this
                this = this.parent
            if this:
                this = this.right
                while this.left:
                    this = this.left
                this.value += to_right
            return True

        if self.left and self.left.reduce_explosion():
            return True
        if self.right and self.right.reduce_explosion():
            return True

    def reduce_split(self):
        if self.value is not None and self.value >= 10:
            self.left = SnailFish()
            self.left.from_str(
                str(self.value // 2),
                self.depth + 1,
                self,
            )
            self.right = SnailFish()
            self.right.from_str(
                str((self.value + 1) // 2),
                self.depth + 1,
                self,
            )
            self.value = None
            return True
        if self.left and self.left.reduce_split():
            return True
        if self.right and self.right.reduce_split():
            return True
        return False

    def reduce(self):
        while self.reduce_explosion() or self.reduce_split():
            pass
        return self

    def __str__(self):
        if self.value is not None:
            return f"{self.value}"
        return f"[{self.left},{self.right}]"

    def __add__(self, other):
        res = SnailFish()
        res.from_snails(self, other)
        return res

    def magnitude(self):
        if self.left:
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()
        return self.value
