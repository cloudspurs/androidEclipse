package server;

import java.io.File;

public class scanFile {
	
	public static void scan(File file) {
		
		String fileList[] = file.list();
		
		if (fileList.length != 0) {
			
			for (int i =0; i < fileList.length; i++) {
				
				String name = file.getAbsolutePath() + "/" +fileList[i];
				File temp = new File(name);
			
				// 如果是文件夹
				if (temp.isDirectory()) {
				
					// 如果文件夹为空
					if (temp.list().length == 0) {
						System.out.println(name + "/");
						continue;
					}
					else {
						scan(temp);
					}
				}
				
				System.out.println(name);
			}
		}
		else {
			String name = file.getAbsolutePath() + "/";
			System.out.println(name);
		}
	}
}