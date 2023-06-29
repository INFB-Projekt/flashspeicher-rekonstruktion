class CRC:

    @staticmethod
    def calc_crc8(hex_string, poly=0x07, init=0x00, ref_in=False, ref_out=False, xor_out=0x00):

        def reflect_byte(byte):
            return int('{:08b}'.format(byte)[::-1], 2)

        data = bytes.fromhex(hex_string)
        crc = init

        for byte in data:
            if ref_in:
                byte = reflect_byte(byte)

            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
                crc &= 0xFF

        if ref_out:
            crc = reflect_byte(crc)

        return f"0x{crc ^ xor_out:02X}"

    @staticmethod
    def isValid(data: str) -> bool:
        crc = "0x"+data[-2:]
        data = data[2:-2]
        # denke aber so besser
        crc_object = CRC()
        calculated_crc = crc_object.calc_crc8(data)

        if crc.upper() == calculated_crc.upper():
            return True
        else:
            return False


if __name__ == "__main__":
    hardware_trace_1 = "0xEEC1020EC6AC1D1F224AA126128ED3334E4E02C5DC3F3AD42A023B77482F0FBB3D370CC144CB456D423F2037FCA8B5F3F134F1CA409AC2BE5C062C23A82B14E7F973B3A27A3786AB1A48405741EC05ED6D9E7068C3768DE3DE82166E5694EA76361C0D21EA0D3330BDF6DDB2F696A733DA890C627395B514B0580A7ED3A56EE618AAE994145CFF97329E2081F9134BB8D98A75D39F75823B0DE9E3879101A72286E3F27F7E9329BE9C6E9FB84820CC8C69AF24D31C1DECB3DF0835D47EC40F177C00B38D9271ED0D5196A1CAABDCAFFDB2A29788C955422C6B551F7CFFBA321E1B19EAA208C60B5D4B2A19F32CE25CA14FD45B2F1647CED8BC4A110F0C766F5C9D5145933E52B76AB6F516E832B87E925C315CAEEE5338D1AB0968A5207D34EE05B59168892A7DEF84F7EB970314D0A627061208AF92295F231D919E94E1641ED742A57F7EB628F0A05ED7E4EEA85EED754C273624EBDFA6D0F9A90C8C8D472D7CC38A50B0DDB3A047DE4FC2928DA23C97F6678AC08648615EE4560DDE733D4D9AFDF3667E2C65181BEFD852E986B5BE92F5A6D9F2D9630A1653E57D56001E8FF342A87C4721A08ADE25F2FB2021A6F58F748475C89D2343226705A650FE83522061D4A17017C3EC9DB7AB8940D8BC6296B74336C195DF6C0EBC8594AC9DF3ED429ACE767A3072DB23F2B7B939F6A4DC3C3126252753FB117D81B306F10B16A339"
    print(CRC.isValid(hardware_trace_1))    #rückgabewert = true
