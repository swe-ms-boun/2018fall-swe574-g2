@tag
Feature: Search test
  Search feature file

  @tag1
  Scenario Outline: Check application is alive
    Given Open firefox browser with "<url>"
    When I search the "<searchitem>"
    Then The searched item should be found
    Examples:
      | url                                           | searchitem |
      | https://aqueous-wildwood-29737.herokuapp.com/ | title      |
      | https://aqueous-wildwood-29737.herokuapp.com/ | game       |