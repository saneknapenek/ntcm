from exception import NumberSystemError
from utils import zfill_list



class Number:

    ASCII_TRANSLATE = 55

    def __init__(self, value: str, system: int = 10) -> None:
        if not isinstance(value, str):
            raise TypeError("The value does not correspond to the number system.")
        if not isinstance(system, int):
            raise TypeError(f"The number system is '{int.__name__}'.\nNot '{system.__class__.__name__}'.")
        inti_value = self.init(value)
        for digit in inti_value:
            if int(digit) >= system:
                raise NumberSystemError(f"The value ({chr(digit + self.ASCII_TRANSLATE)}) does not correspond to the number system ({system})")
        self.__value = inti_value
        self.system = system

    @classmethod
    def init(cls, value: str) -> list[int]:
        return list(map(lambda d: int(ord(d) - cls.ASCII_TRANSLATE) if not d.isdigit() else int(d), value))
    
    @classmethod
    def __to_str(cls, lst: list[int]) -> str:
        return "".join(map(lambda d: str(chr(d + cls.ASCII_TRANSLATE)) if d >= 10 else str(d), lst))
    
    def __str__(self) -> str:
        return self.__to_str(self.__value)
    
    def __repr__(self) -> list[int]:
        return self.__str__()
    
    def __len__(self) -> int:
        return len(self.__value)
    
    def __eq__(self, out_obj) -> bool:
        self.__check_out_obj(out_obj)
        self.__check_out_system(out_obj)
        if self.__value == out_obj.__value:
            return True
        return False
    
    def __ne__(self, out_obj) -> bool:
        return not self.__eq__(out_obj)
    
    def __gt__(self, out_obj) -> bool:
        self.__check_out_obj(out_obj)
        self.__check_out_system(out_obj)
        if len(self) > len(out_obj):
            return True
        if len(self) < len(out_obj):
            return False
        for i in range(len(self)):
            if self.__value[i] > out_obj.__value[i]:
                return True
            elif self.__value[i] < out_obj.__value[i]:
                return False
        return False

    def __lt__(self, out_obj) -> bool:
        self.__check_out_obj(out_obj)
        self.__check_out_system(out_obj)
        if len(self) < len(out_obj):
            return True
        if len(self) > len(out_obj):
            return False
        for i in range(len(self)):
            if self.__value[i] < out_obj.__value[i]:
                return True
            elif self.__value[i] > out_obj.__value[i]:
                return False
        return False
    
    def __ge__(self, out_obj) -> bool:
        return not self.__lt__(out_obj)
    
    def __le__(self, out_obj) -> bool:
        return not self.__gt__(out_obj)
    
#------------------algorithms------------------
    def __add__(self, out_obj):
        self.__check_out_obj(out_obj)
        self.__check_out_system(out_obj)
        max_len = max(len(self), len(out_obj))
        number1 = zfill_list(self.__value, max_len)
        number2 = zfill_list(out_obj.__value, max_len)
        carry = 0
        result = []

        for i in range(max_len - 1, -1, -1):
            temp_sum = number1[i] + number2[i] + carry
            carry = temp_sum // self.system
            result.append(temp_sum % self.system)

        if carry:
            result.append(carry)
        
        return self.__class__(self.__to_str(reversed(result)), system=self.system)
    
    def __radd__(self, out_obj):
        return self.__class__(out_obj).__add__(self)
    
    def __sub__(self, out_obj):
        self.__check_out_obj(out_obj)
        self.__check_out_system(out_obj)
        max_len = max(len(self), len(out_obj))
        if self < out_obj: #! - ?
            number1 = zfill_list(out_obj.__value, max_len)
            number2 = zfill_list(self.__value, max_len)
        else:
            number1 = zfill_list(self.__value, max_len)
            number2 = zfill_list(out_obj.__value, max_len)
        borrow = 0
        result = []

        for i in range(max_len - 1, -1, -1):
            temp_diff = number1[i] - number2[i] - borrow

            if temp_diff < 0:
                temp_diff += self.system
                borrow = 1
            else:
                borrow = 0

            result.append(temp_diff)

        return self.__class__(self.__to_str(reversed(result)), system=self.system)

    def __rsub__(self, out_obj):
        return self.out_obj.__sub__(self)
    
    def __mul__(self, out_obj):
        number1 = self.__value
        number2 = out_obj.__value
        result = [0] * (len(self) + len(out_obj))

        for i in range(len(self) - 1, -1, -1):
            carry = 0

            for j in range(len(out_obj) - 1, -1, -1):
                temp_sum = number1[i] * number2[j] + result[i + j + 1] + carry
                carry = temp_sum // self.system
                result[i + j + 1] = temp_sum % self.system

            result[i] += carry

        while result and result[0] == 0:
            result.pop(0)
        if result:
            return self.__class__(self.__to_str(result), system=self.system)
        else:
            return self.__class__("0", system=self.system)
    
    def __rmul__(self, out_obj):
        return self.__class__(out_obj).__mul__(self)
    
    def __truediv__(self, out_obj):
        number1 = self.to_decimal()
        number2 = out_obj.to_decimal()

        quotient = self.__class__(self.__to_str(map(int, list(str(number1 // number2)))))
        remainder = self.__class__(self.__to_str(map(int, list(str(number1 % number2)))))

        quotient.to_any(self.system)
        remainder.to_any(self.system)

        return quotient, remainder

    def __rtruediv__(self, out_obj):
        return self.__class__(out_obj).__div__(self)
#----------------------------------------------

    def __check_out_system(self, out_obj):
        if out_obj.system != self.system:
            raise ValueError("Does not support different number systems")
                
    def __check_out_obj(self, obj):
        if not isinstance(obj, self.__class__):
            raise TypeError(f"Unsupported {obj.__class__}")
    
    def to_decimal(self) -> int:
        if self.system == 10:
            return int("".join(map(str, self.__value)))
        decimal_num = 0
        power = 0
        for digit in reversed(self.__value):
            decimal_num += digit * (self.system ** power)
            power += 1
        return decimal_num
    
    def to_any(self, system) -> None:
            
        result = []
        dec = self.to_decimal()
        while dec > 0:
            remainder = dec % system
            result.insert(0, remainder)
            dec = dec // system
        self.__value = result



obj1 = Number("F1234567890123456789012345678901234567890", 16)
obj2 = Number("9876543210987654321098765432109876543210A", 16)

print(obj1 > obj2)
print(obj1 < obj2)
print(obj1 >= obj2)
print(obj1 <= obj2)

print(obj1 + obj2)
print(obj1 - obj2)
print(obj1 * obj2)
print(obj1 / obj2)
