import java.io.BufferedReader;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;

import com.opensymphony.xwork2.ActionSupport;

public class RLExample1Action extends ActionSupport {
	private static final long serialVersionUID = 1L;
	
	public String execute() throws Exception {
		File dir = new File("/usr/local/tomcat8/webapps/Android/RelFix");
		String dirApk = "./RelFix.py Apks/Benchmarks/onClick/onClick.apk";
		
		String[] cmd = {"/bin/sh", "-c", dirApk};  
        Process pro = Runtime.getRuntime().exec(cmd, null, dir);  
        pro.waitFor();  
        InputStream in = pro.getInputStream();  
        BufferedReader read = new BufferedReader(new InputStreamReader(in));  
        String line = null;  
        while((line = read.readLine())!=null){  
            System.out.println(line);  
        }
		
        /*
        String[] command = {"/bin/sh", "-c", dirApk};  
        Process process = Runtime.getRuntime().exec(command);  
        process.waitFor();  
        InputStream input = process.getInputStream();  
        BufferedReader br = new BufferedReader(new InputStreamReader(input));  
        String newLine = null;  
        while((newLine = br.readLine())!=null){  
            System.out.println(newLine);  
        }
        */
        
		return "success";
	}
}
