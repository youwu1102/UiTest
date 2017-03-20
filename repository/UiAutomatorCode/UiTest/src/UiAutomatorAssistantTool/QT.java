package UiAutomatorAssistantTool;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class QT {

	private static String android_id = "10";
	private static String jar_name = "";
	private static String test_class = "";
	private static String test_name = "";

	private static String workspace_path;
	private static String bundle_key = "";
	private static String bundle_keyvalue = "";

    public static void main(String[] args) {
		
	}
	public QT() {
		workspace_path = getWorkSpase();
	}
	public QT(String jarName, String testClass, String testName,
			String androidId) {
		System.out.println("*******************");
		System.out.println("----START DEBUG----");
		System.out.println("*******************");
		workspace_path = getWorkSpase();
		jar_name = jarName;
		test_class = testClass;
		test_name = testName;
		android_id = androidId;
		runUiautomator();
		System.out.println("*******************");
		System.out.println("---FINISH DEBUG----");
		System.out.println("*******************");
	}
	public QT(String jarName, String testClass, String testName,
			String androidId,String Key,String KeyValue) {
		System.out.println("*******************");
		System.out.println("----START DEBUG----");
		System.out.println("*******************");
		workspace_path = getWorkSpase();
		jar_name = jarName;
		test_class = testClass;
		test_name = testName;
		android_id = androidId;
		bundle_key = Key;
		bundle_keyvalue = KeyValue;
		
		runUiautomator();
		System.out.println("*******************");
		System.out.println("---FINISH DEBUG----");
		System.out.println("*******************");
	}

	private void runUiautomator() {
		creatBuildXml();
		modfileBuild();
		buildWithAnt();
		if (System.getProperty("os.name").equals("Linux")) {
			pushTestJar(workspace_path + "/bin/" + jar_name + ".jar");
		}else{
		pushTestJar(workspace_path + "\\bin\\" + jar_name + ".jar");
		}
		
		if (test_name.equals("")) {
			if(bundle_key.equals(""))
			{
				runTest(jar_name, test_class);
			}
			else
			{
				runTest(jar_name, test_class,bundle_key,bundle_keyvalue);
			}
			
		}else{
			if(bundle_key.equals(""))
			{
				runTest(jar_name, test_class + "#" + test_name);
			}
			else
			{
				runTest(jar_name, test_class + "#" + test_name,bundle_key,bundle_keyvalue);
			}
		}
		
		
	}		


	// 1--判断是否有build
	public boolean isBuild() {
		File buildFile = new File("build.xml");
		if (buildFile.exists()) {
			return true;
		}
		// 创建build.xml
		execCmd("cmd /c android create uitest-project -n " + jar_name + " -t "
				+ android_id + " -p " + workspace_path);
		return false;
	}

	// 创建build.xml
	public void creatBuildXml() {
		execCmd("cmd /c android create uitest-project -n " + jar_name + " -t "
				+ android_id + " -p " + "\""+workspace_path+ "\"");
	}

	// 2---build
	public void modfileBuild() {
		StringBuffer stringBuffer = new StringBuffer();
		try {
			File file = new File("build.xml");
			if (file.isFile() && file.exists()) { // 判断文件是否存在
				InputStreamReader read = new InputStreamReader(
						new FileInputStream(file));
				BufferedReader bufferedReader = new BufferedReader(read);
				String lineTxt = null;
				while ((lineTxt = bufferedReader.readLine()) != null) {
					if (lineTxt.matches(".*help.*")) {
						lineTxt = lineTxt.replaceAll("help", "build");
					}
					stringBuffer = stringBuffer.append(lineTxt + "\t\n");
				}
				read.close();
			} else {
				System.out.println("找不到指定的文件");
			}
		} catch (Exception e) {
			System.out.println("读取文件内容出错");
			e.printStackTrace();
		}
		writerText("build.xml", new String(stringBuffer));
	}

	

	// 3---ant build
	public void buildWithAnt() {
		if (System.getProperty("os.name").equals("Linux")) {
			execCmd("ant");
			return;
		}
		execCmd("cmd /c ant");
	}

	// 4---push jar
	public void pushTestJar(String localPath) {
		localPath="\""+localPath+"\"";
		String pushCmd = "adb push " + localPath + " /data/local/tmp/";
		execCmd(pushCmd);
	}
	
	public void runTest(String jarName, String testName) {
		String runCmd = "adb shell uiautomator runtest ";
		String testCmd = jarName + ".jar -c "+ testName;
		System.out.println(testCmd);
		execCmd(runCmd + testCmd);
	}
	public void runTest(String jarName, String testName,String Key,String KeyValue) {
		String runCmd = "adb shell uiautomator runtest ";
		String testCmd = jarName + ".jar -c "+ testName + " -e "+Key+" "+KeyValue;
		System.out.println(testCmd);
		execCmd(runCmd + testCmd);
	}
	
	
	
	

	public String getWorkSpase() {
		File directory = new File("");
		String abPath = directory.getAbsolutePath();
		return abPath;
	}
	
	public void execCmd(String cmd) {
		try {
			Process p = Runtime.getRuntime().exec(cmd);
			InputStream input = p.getInputStream();
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					input));
			String line = "";
			while ((line = reader.readLine()) != null) {
					
				System.out.println(line.replace("\r\n",""));
                saveToFile(line, "runlog.log", false);
			}
			//错误输出流
			InputStream errorInput = p.getErrorStream();
			BufferedReader errorReader = new BufferedReader(new InputStreamReader(
					errorInput));
			String eline = "";
			while ((eline = errorReader.readLine()) != null) {
				System.out.println(eline);
                saveToFile(eline, "runlog.log", false);
			}       
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	public void writerText(String path, String content) {

		File dirFile = new File(path);

		if (!dirFile.exists()) {
			dirFile.mkdir();
		}

		try {
			// new FileWriter(path + "t.txt", true) 这里加入true 可以不覆盖原有TXT文件内容 续写
			BufferedWriter bw1 = new BufferedWriter(new FileWriter(path));
			bw1.write(content);
			bw1.flush();
			bw1.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

    public void saveToFile(String text,String path,boolean isClose) {
    	File file=new File("runlog.log");   	
		BufferedWriter bf=null;
		try {
		    FileOutputStream outputStream=new FileOutputStream(file,true);
		    OutputStreamWriter outWriter=new OutputStreamWriter(outputStream);
		    bf=new BufferedWriter(outWriter);
			bf.append(text);
			bf.newLine();
			bf.flush();
			
			if(isClose){
				bf.close();
			}
		} catch (FileNotFoundException e1) {
			e1.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		
	}


	

}