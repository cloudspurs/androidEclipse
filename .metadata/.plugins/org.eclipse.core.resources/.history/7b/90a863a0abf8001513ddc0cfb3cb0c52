package server;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.Writer;
import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.dom4j.io.XMLWriter;

public class xmlAction {
	 
	public static void createXml(userInfo userinfo, String file) {
		
        try {
        	
            // 创建Document对象  
            Document document = DocumentHelper.createDocument();  
            
            // 添加根节点users
            Element root = document.addElement("users");  
            
            // 添加子节点email
            Element email = root.addElement("email"); 
            email.setText(userinfo.getEmail());
            
            // 添加子节点file
            Element filename = root.addElement("filename");
            filename.setText(userinfo.getFile());
            
            // 将document文档写入user.xml文件
            Writer fileWriter = new FileWriter(file);
            
            //dom4j提供了专门写入文件的对象XMLWriter  
            XMLWriter xmlWriter = new XMLWriter(fileWriter);  
          
            xmlWriter.write(document);  
            xmlWriter.flush();  
            xmlWriter.close();
            
            // 将document文档对象直接转换成字符串输出 
            System.out.println(document.asXML());
            
            System.out.println("xml文档添加成功！");  
            
        } catch (IOException e) {  
            e.printStackTrace();  
        }  
	}
	
	public static userInfo readXml(String file){
		
		userInfo userinfo = new userInfo();
        try{
        	InputStream inputStream = new FileInputStream(new File(file));
        	
        	//新建SaxReader对象，读取XML文档   
            SAXReader saxReader = new SAXReader();
               
            Document document = saxReader.read(inputStream);	 
            
            //获取根节点对象  
            Element root = document.getRootElement();
            
            //获取email子节点  
            Element email = root.element("email");  
            if(email != null){  
            	userinfo.setEmail(email.getText());
            }
            
            // 获取filename子节点
            Element filename = root.element("filename");  
            if(filename != null){  
            	userinfo.setFile(filename.getText());
            }
            
        } catch (Exception e) {    
            e.printStackTrace();    
        }
        
        return userinfo;
    }

}

 