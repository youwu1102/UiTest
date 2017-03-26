from Utility import Utility
from GlobalVariable import GlobalVariable
import time

class TestMain(object):
    def __init__(self, log_path, xml_store_path):
        self.log_path = log_path

    def run(self):
        thread_push_blank_file = threading.Thread(target=Utility.push_action_file_to_device,
                                                  args=(GlobalVariable.blank_action_file,))
        thread_push_blank_file.start()
        Utility.pull_dump_file_to_pc(local=self.xml_store_path)
        Utility.output_msg('I pulled dump file to pc and I will start parse dump file')
        eigenvalue = Utility.analysis_dump(self.xml_store_path)
        actions = GlobalVariable.dict_dump_actions.get(eigenvalue)
        if len(actions) > 0:
            steps = actions[0]
            del actions[0]
            with open('tmp.txt', 'w') as action_file:
                for step in steps:
                    print step.encode('utf-8')
                    action_file.write(step.encode('utf-8') + '\n')
        else:
            step = '%04d,\t' % (6+len('BACK')) + 'BACK' + '\n'
            with open('tmp.txt', 'w') as action_file:
                action_file.write(step)
                action_file.close()
        Utility.run_command_on_pc('adb push tmp.txt /data/local/tmp/Action.txt')
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