import itertools


def find_loop_size(public_key: int) -> int:
    sub_num = 7
    value = 1
    for loop_size in itertools.count():
        value = value * sub_num
        value = value % 20201227
        if value == public_key:
            return loop_size


def find_encryption(public_key: int, loop_size: int) -> int:
    encryption_key = 1
    for i in range(loop_size):
        encryption_key = encryption_key * public_key
        encryption_key = encryption_key % 20201227
    return encryption_key


#
# Unit tests
#
test_public_keys = [5764801, 17807724]
loop_size_0 = find_loop_size(test_public_keys[0])
loop_size_1 = find_loop_size(test_public_keys[1])
encryption_key_0 = find_encryption(test_public_keys[1], loop_size_0 + 1)
encryption_key_1 = find_encryption(test_public_keys[0], loop_size_1 + 1)

assert encryption_key_0 == encryption_key_1

#
# Problem
#

public_keys = [15113849, 4206373]

loop_size_0 = find_loop_size(public_keys[0])
loop_size_1 = find_loop_size(public_keys[1])
encryption_key_0 = find_encryption(public_keys[1], loop_size_0 + 1)
encryption_key_1 = find_encryption(public_keys[0], loop_size_1 + 1)

assert encryption_key_0 == encryption_key_1
print(encryption_key_0)
