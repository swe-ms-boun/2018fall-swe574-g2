#Sample Feature Definition Template
@tag
Feature: Thymesis smoke test
  My feature file

  @tag1
  Scenario Outline: Check application is alive
    Given Open firefox browser
    When I enter the "<url>"
    Then The web page should be open

    Examples:
      | url                                           |
      | https://aqueous-wildwood-29737.herokuapp.com/ |
