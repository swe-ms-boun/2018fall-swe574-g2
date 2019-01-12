@tag
Feature: Login Tests
  My feature file
  @tag1
  Scenario Outline: Login
    Given I enter the url as "<url>"
    When Open the toggle bar
    When I enter username as "<username>"
    When I enter password as "<password>"
    When Click login button
    Then User should be able to login successfully
    Examples:
      | url                                           | username | password |
      | https://aqueous-wildwood-29737.herokuapp.com/ | deno     | 123456   |
  @tag1
  Scenario Outline: Login Unsuccessful
    Given I enter the url as "<url>"
    When Open the toggle bar
    When I enter username as "<username>"
    When I enter password as "<password>"
    When Click login button
    Then User should not be able to login
    Examples:
      | url                                           | username | password |
      | https://aqueous-wildwood-29737.herokuapp.com/ | lalal    | wrong    |