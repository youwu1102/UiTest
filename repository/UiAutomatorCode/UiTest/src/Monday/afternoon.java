package Monday;

import java.util.ArrayList;
import com.android.uiautomator.core.UiDevice;
import com.android.uiautomator.core.UiObjectNotFoundException;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;
import Monday.morning;
import UiAutomatorAssistantTool.QT;

public class afternoon extends UiAutomatorTestCase {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String jarName = "Demo";
		String testClass = "Monday.afternoon";
		String testName = "test3rd_App";
		String androidId = "11";
		new QT(jarName, testClass, testName, androidId);
	}

	public void test3rd_App() {

		UiDevice device = getUiDevice();
		device.setCompressedLayoutHeirarchy(true);
		morning morn = new morning();
		while (true) {
			try {
				getUiDevice().dumpWindowHierarchy("current.xml");
			} catch (java.lang.NullPointerException e) {
				System.out.println("STATE:DumpException");
			} catch (java.lang.IllegalArgumentException e) {
				System.out.println("STATE:DumpException");
			}
			System.out.println("STATE:WAIT");
			sleep(1000);
			ArrayList<String> actions = morning
					.getActions("/data/local/tmp/Action.txt");
			if (actions.size() == 0) {
				System.out.println("STATE:EMPTY");
				continue;
			}
			if (morning.isLegal(actions)) {
				for (String action : actions) {
					try {
						morn.parse_action(action, device);
					} catch (UiObjectNotFoundException e) {
						System.out.println("STATE:UiObjectNotFoundException");
						continue;
					}
				}
				System.out.println("STATE:DONE");
			} else {
				System.out.println("STATE:ILLEGAL");
			}
		}
	}
}
