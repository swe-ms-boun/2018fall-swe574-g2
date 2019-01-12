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

public class LoginTests {
    WebDriver driver;

    @Given("^I enter the url as \"([^\"]*)\"$")
    public void i_enter_the_url_as(String url) throws Throwable {
        System.setProperty("webdriver.gecko.driver", "resource/geckodriver");
        driver = new FirefoxDriver();
        driver.manage().window().maximize();
        driver.get(url);
        WebDriverWait wait = new WebDriverWait(driver, 10);
        WebElement searchButton = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".input-group-append")));
        Assert.assertEquals(searchButton.getText(), "Search");
    }

    @When("^Open the toggle bar")
    public void open_toggle_bar() throws Throwable {
        try {
            WebDriverWait wait = new WebDriverWait(driver, 10);
            WebElement searchButton = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".navbar-toggler-icon")));
            Assert.assertNotNull(searchButton.getSize());
        } catch (Exception ex) {
            System.out.println("No need to click toggle button.. Continue");
        }
    }

    @When("^I enter username as \"([^\"]*)\"$")
    public void i_enter_username(String given_username) throws Throwable {
        WebDriverWait wait = new WebDriverWait(driver, 10);
        WebElement username = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("input[name=\"username\"]")));
        username.sendKeys(given_username);
    }

    @When("^I enter password as \"([^\"]*)\"$")
    public void i_enter_password(String given_password) throws Throwable {
        WebDriverWait wait = new WebDriverWait(driver, 10);
        WebElement password = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("input[name=\"password\"]")));
        password.sendKeys(given_password);
    }

    @When("^Click login button$")
    public void click_login_button() throws Throwable {
        WebDriverWait wait = new WebDriverWait(driver, 10);
        WebElement loginButton = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("button[type=\"submit\"]:nth-child(3)")));
        loginButton.click();
    }

    @Then("^User should be able to login successfully$")
    public void web_page_openasasa() throws Throwable {
        WebDriverWait wait = new WebDriverWait(driver, 10);
        WebElement logoutButton = wait.until(ExpectedConditions.elementToBeClickable(By.linkText("Logout")));
        Assert.assertNotNull(logoutButton);
        driver.quit();
    }

    @Then("^User should not be able to login")
    public void not_open() throws Throwable {
        WebElement logoutButton = null;
        try {
            logoutButton = driver.findElement(By.linkText("Logout"));
        } catch (Exception ex) {
            Assert.assertNull(logoutButton);
        }
        driver.quit();
    }
}
