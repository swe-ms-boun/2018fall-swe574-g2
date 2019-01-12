package test_steps;

import cucumber.api.java.en.When;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import cucumber.api.java.en.Given;
import org.openqa.selenium.firefox.FirefoxDriver;
import cucumber.api.java.en.Then;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;


public class WebSmokeTests {
    WebDriver driver;

    @Given("^Open firefox browser$")
    public void open_firefox_browser() throws Throwable {
        System.setProperty("webdriver.gecko.driver", "resource/geckodriver");
        driver = new FirefoxDriver();
        driver.manage().window().maximize();
    }


    @When("^I enter the \"([^\"]*)\"$")
    public void i_enter_the(String url) throws Throwable {
        driver.get(url);
        WebDriverWait wait = new WebDriverWait(driver, 10);
        WebElement searchButton = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".input-group-append")));
        Assert.assertEquals(searchButton.getText(), "Search");
    }


    @Then("^The web page should be open$")
    public void web_page_open() throws Throwable {
        driver.getPageSource().contains("Thymesis");
        driver.quit();
    }
}
