package test_steps;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.Keys;

public class MemoryTests {
    WebDriver driver;

    @Given("^Open firefox browser with \"([^\"]*)\"$")
    public void open_browser_with(String url) throws Throwable {
        System.setProperty("webdriver.gecko.driver", "resource/geckodriver");
        driver = new FirefoxDriver();
        driver.manage().window().maximize();
        driver.get(url);
        WebDriverWait wait = new WebDriverWait(driver, 10);
        WebElement searchButton = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".input-group-append")));
        Assert.assertEquals(searchButton.getText(), "Search");
    }

    @When("^I search the \\\"([^\\\"]*)\\\"$")
    public void search_item(String searchItem) throws Throwable {
        WebDriverWait wait = new WebDriverWait(driver, 10);
        WebElement searchBar = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("input[placeholder=\"Search memories...\"]")));
        searchBar.sendKeys(searchItem);
        searchBar.sendKeys(Keys.RETURN);
    }

    @Then("^The searched item should be found$")
    public void web_page_openasasa() throws Throwable {
        WebDriverWait wait = new WebDriverWait(driver, 10);
        WebElement memoryTitle = wait.until(ExpectedConditions.elementToBeClickable(By.className("card-header")));
        Assert.assertNotNull(memoryTitle);
        driver.quit();
    }
}
