from exception import NumberSystemError



class Number:

    def __init__(self, value: str, system: int = 10) -> None:
        if not isinstance(value, str):
            raise TypeError("The value does not correspond to the number system.")
        if not isinstance(system, int):
            raise TypeError(f"The number system is '{int.__name__}'.\nNot '{system.__class__.__name__}'.")
        for digit in value:
            if int(digit) >= system:
                raise NumberSystemError("The value does not correspond to the number system")
        self.__value = value
        self.system = system
    
    def __str__(self) -> str:
        return self.__value
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return len(self.__value)
    
    def __eq__(self, out_obj) -> bool:
        self.__check_out_obj(out_obj)
        self.__check_out_system(out_obj)
        if str(self) == str(out_obj):
            return True
        return False
    
    def __ne__(self, out_obj) -> bool:
        return not self.__eq__(out_obj)
    
    def __ge__(self, out_obj) -> bool:
        self.__check_out_obj(out_obj)
        self.__check_out_system(out_obj)
        if len(self) < len(out_obj):
            return False
        if len(self) > len(out_obj):
            return True
        for i in range(len(self)-1, -1, -1):
            if str(self)[i] < str(out_obj)[i]:  #!
                return False
        return True
    
    def __lt__(self, out_obj) -> bool:
        return not self.__ge__(out_obj)
    
    def __le__(self, out_obj) -> bool:
        self.__check_out_obj(out_obj)
        self.__check_out_system(out_obj)
        if len(self) < len(out_obj):
            return True
        if len(self) > len(out_obj):
            return False
        for i in range(len(self)-1, -1, -1):
            if str(self)[i] > str(out_obj)[i]:
                return False
        return True
    
    def __gt__(self, out_obj) -> bool:
        return not self.__le__(out_obj)
    
#------------------algorithms------------------
    def __add__(self, out_obj):
        self.__check_out_obj(out_obj)
        self.__check_out_system(out_obj)
        max_len = max(len(self), len(out_obj))
        number1 = str(self).zfill(max_len)
        number2 = str(out_obj).zfill(max_len)
        carry = 0
        result = []

        for i in range(max_len - 1, -1, -1):
            temp_sum = int(number1[i]) + int(number2[i]) + carry
            carry = temp_sum // self.system
            result.append(str(temp_sum % self.system))

        if carry:
            result.append(str(carry))

        return self.__class__(''.join(result[::-1]), system=self.system)
    
    def __radd__(self, out_obj):
        return self.__class__(out_obj).__add__(self)
    
    def __sub__(self, out_obj):
        self.__check_out_obj(out_obj)
        self.__check_out_system(out_obj)
        max_len = max(len(self), len(out_obj))
        if self < out_obj: #! - ?
            number1 = str(out_obj).zfill(max_len)
            number2 = str(self).zfill(max_len)
        else:
            number1 = str(self).zfill(max_len)
            number2 = str(out_obj).zfill(max_len)
        borrow = 0
        result = []

        for i in range(max_len - 1, -1, -1):
            temp_diff = int(number1[i]) - int(number2[i]) - borrow

            if temp_diff < 0:
                temp_diff += self.system
                borrow = 1
            else:
                borrow = 0

            result.append(str(temp_diff))

        return self.__class__(''.join(result[::-1]), system=self.system)

    def __rsub__(self, out_obj):
        return self.out_obj.__sub__(self)
    
    def __mul__(self, out_obj):
        number1 = str(self)
        number2 = str(out_obj)
        result = [0] * (len(self) + len(out_obj))

        for i in range(len(self) - 1, -1, -1):
            carry = 0

            for j in range(len(out_obj) - 1, -1, -1):
                temp_sum = int(number1[i]) * int(number2[j]) + result[i + j + 1] + carry
                carry = temp_sum // self.system
                result[i + j + 1] = temp_sum % self.system

            result[i] += carry

        result_str = ''.join(map(str, result))
        return self.__class__(result_str.lstrip('0') or '0')
    
    def __rmul__(self, out_obj):
        return self.__class__(out_obj).__mul__(self)
    
    def __truediv__(self, out_obj):
        number1 = int(self.to_decimal())
        number2 = int(out_obj.to_decimal())

        quotient = number1 // number2
        remainder = number1 % number2

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
        
    def to_decimal(self):
        if self.system == 10:
            return str(self)
        decimal_num = 0
        power = 0
        for digit in str(self)[::-1]:
            decimal_num += int(digit) * (int(self.system) ** power)
            power += 1
        return str(decimal_num)
    
    def to_any(self, system):
        if self.system != 10:
            self.to_decimal()
        
        result = ""
        dec = int(str(self))
        while dec > 0:
            remainder = dec % system
            result = str(remainder) + result
            dec = dec // system
        return str(result)


# obj1 = Number("1234567890123456789012345678901234567890")
# obj2 = Number("9876543210987654321098765432109876543210")

# print(obj1 + obj2)
# print(obj1 - obj2)
# print(obj1 * obj2)
# print()
# obj1 = Number("101252434323123124", 6)
# obj2 = Number("1012524343", 6)

# print(obj1 + obj2)
# print(obj1 - obj2)
# print(obj1 * obj2)

# print(obj1 + obj2)
# print(obj1 - obj2)
# print(obj1 * obj2)

obj1 = Number("1234567890123456789012345678901234567890")
obj2 = Number("9876543210987654321098765432109876543210")

print(obj1 + obj2)
print(obj1 - obj2)
print(obj1 * obj2)
print(obj1 / obj2)
