__author__ = 'c_youwu'
from Utility import Utility
import threading
from GlobalVariable import GlobalVariable
import time

class TestMain(threading.Thread):
    def __init__(self, log_path, xml_store_path):
        self.log_path = log_path
        self.xml_store_path = xml_store_path
        threading.Thread.__init__(self)

    def run(self):
        thread_push_blank_file = threading.Thread(target=Utility.push_action_file_to_device,
                                                  args=(GlobalVariable.blank_action_file,))
        thread_push_blank_file.start()
        Utility.pull_dump_file_to_pc(local=self.xml_store_path)
        Utility.output_msg('I pulled dump file to pc and I will start parse dump file')
        Utility.analysis_dump(self.xml_store_path)
        Utility.output_msg('TestMain:Done %s ' % time.time())


        # thread1=thread.start_new_thread()
        # thread.start_new_thread(ApplicationClassification.pull_dump_to_pc, (self.xml_store_path,))





if __name__ == '__main__':
    import time
    start = time.time()
    import os
    #p = 'C:\\Users\\wuyou\\Desktop\\UiTest\\logs\\tmp'
    p = 'C:\\cygwin64\\home\\c_youwu\\UiTest\\logs\\tmp'
    for f in os.listdir(p):
        ApplicationClassification.analysis_dump(os.path.join(p, f))
    print time.time()-start