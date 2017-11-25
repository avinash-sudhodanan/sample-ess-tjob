import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.remote.DesiredCapabilities;

public class MyTest {

  Capabilities chromeCapabilities = DesiredCapabilities.chrome();
  

  public static void main() {
    WebDriver chrome = new RemoteWebDriver(new URL(System.getenv("ET_EUS_API")), chromeCapabilities);
    // run against chrome
    chrome.get("https://www.google.com");
    System.out.println(chrome.getTitle());
    chrome.quit();
  
  }
}
