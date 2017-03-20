package Monday;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

import com.android.uiautomator.core.UiDevice;
import com.android.uiautomator.core.UiObject;
import com.android.uiautomator.core.UiObjectNotFoundException;
import com.android.uiautomator.core.UiSelector;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;

public class morning extends UiAutomatorTestCase{

	public static ArrayList<String> getActions(String fileName) {
		File file = new File(fileName);
		BufferedReader reader = null;
		ArrayList<String> actions = new ArrayList<String>();
		try {
			reader = new BufferedReader(new FileReader(file));
			String tempString = null;
			while ((tempString = reader.readLine()) != null) {
				actions.add(tempString);
			}
			reader.close();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return actions;
	}

	public static String[] getPackagename(String fileName) {
		File file = new File(fileName);
		BufferedReader reader = null;
		String[] tempString = new String[2];
		try {
			reader = new BufferedReader(new FileReader(file));
			tempString[0] = reader.readLine();
			tempString[1] = reader.readLine();
			reader.close();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return tempString;
	}

	public void parse_action(String action, UiDevice device)
			throws UiObjectNotFoundException {
		String[] string_list = action.split(",\t");
		switch (string_list[1]) {
		case "EDIT":
			Edit(string_list);
			break;
		case "CLICK":
			Click(string_list);
			break;
		case "TOUCH":
			System.out.println("pretend I touch something");
			break;
		case "BACK":
			device.pressBack();
			break;
		case "START":
			Start(string_list);
			sleep(3000);
		default:
			System.out.println("STATE:UnknowAction<" + action + ">");
			break;
		}

	}

	public static void Edit(String[] string_list)
			throws UiObjectNotFoundException {
		UiObject object = new UiObject(getSelector(string_list));
		object.setText(string_list[1]);
		System.out.println("STATE:UiObjectNotFoundException");

	}

	public static void Click(String[] string_list)
			throws UiObjectNotFoundException {
		UiObject object = new UiObject(getSelector(string_list));
		object.clickAndWaitForNewWindow();

	}
	
	public static void Start(String[] string_list) {
		if (string_list[2].endsWith(""))
		{
			startApp(string_list[1]);
		}
		else
		{
			startApp(string_list);
		}

	}
	
	private static void startApp(String[] string_list) {
		try {
			Runtime.getRuntime().exec(
					"am start -n " + string_list[1] + "/" + string_list[2]);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	private static void startApp(String app) {
		try {
			Runtime.getRuntime().exec("am start " + app);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static UiSelector getSelector(String[] string_list) {
		// check code = string_list[0]
		// action = string_list[1]
		// value = string_list[2]
		// text = string_list[3]
		// resourceId=string_list[4]
		// description=string_list[5]
		// className=string_list[6]

		UiSelector selector = new UiSelector();
		if (!string_list[3].equals("")) {
			System.out.println("text:" + string_list[3]);
			selector = selector.text(string_list[3]);
		}
		if (!string_list[4].equals("")) {
			System.out.println("resourceId:" + string_list[4]);
			selector = selector.resourceId(string_list[4]);
		}
		if (!string_list[5].equals("")) {
			System.out.println("description:" + string_list[5]);
			selector = selector.description(string_list[5]);
		}
		if (!string_list[6].equals("")) {
			System.out.println("className:" + string_list[6]);
			selector = selector.className(string_list[6]);
		}
		return selector;
	}

	public static boolean isLegal(ArrayList<String> actions) {
		int check_code;
		for (String action : actions) {
			String[] string_list = action.split(",\t");
			System.out.println(string_list[0]);
			System.out.println(action.length());
			try {
				check_code = Integer.parseInt(string_list[0]);
				if (check_code != action.length()) {
					return false;
				}
			} catch (java.lang.NumberFormatException e) {
				return false;
			}
		}
		return true;
	}
}
