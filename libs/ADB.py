__author__ = 'c_youwu'


class Adb(object):
    adb_exe = 'adb'

    @staticmethod
    def pull(remote, local, serial_number=''):
        if serial_number:
            return '{adb} -s {serial_number} pull {remote} {local}'.format(adb=Adb.adb_exe,
                                                                           serial_number=serial_number,
                                                                           remote=remote, local=local)
        return '{adb} pull {remote} {local}'.format(adb=Adb.adb_exe, remote=remote, local=local)

    @staticmethod
    def push(local, remote, serial_number=''):
        if serial_number:
            return '{adb} -s {serial_number} push {local} {remote}'.format(adb=Adb.adb_exe,
                                                                           serial_number=serial_number,
                                                                           remote=remote, local=local)
        return '{adb} push {local} {remote}'.format(adb=Adb.adb_exe, remote=remote, local=local)

    @staticmethod
    def reboot(serial_number='', mode=''):
        if serial_number:
            if mode:
                return '{adb} -s {serial_number} reboot-{mode}'.format(adb=Adb.adb_exe, serial_number=serial_number, mode=mode)
            return '{adb} -s {serial_number} reboot'.format(adb=Adb.adb_exe, serial_number=serial_number)
        if mode:
            return '{adb} reboot-{mode}'.format(adb=Adb.adb_exe, mode=mode)
        return '{adb} reboot'.format(adb=Adb.adb_exe)

    @staticmethod
    def wait_for_device(serial_number):
        if serial_number:
            return '{adb} -s {serial_number} wait-for-device'.format(adb=Adb.adb_exe, serial_number=serial_number)
        return '{adb} wait-for-device'.format(adb=Adb.adb_exe)

if __name__ == '__main__':
    print Adb.push(remote='C:\\1\\1.txt',local='/mnt/sdcard/')