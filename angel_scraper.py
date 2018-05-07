string = """

Apply to Hush
We're creating the best beauty experience on mobile
Los Angeles, 11-50 employees, Active this week, 38 applicants last week
Profile
Profile avatar
Catherine Han
Fullstack Engineer seeking opportunity in web development.
Position
Software Engineer (Frontend)
Los Angeles ·Full Time· $100K - $130K· 0.1% - 0.5%
Skills
Javascript, CSS, React.js
Contact
Profile avatar
William King

""".split('\n')

def get_skills(string):
  string = '\n'.join(string).lower()
  ret = ['React/Redux', 'CSS3/Sass', 'Node.js', 'Django', 'Postgres', 'Heroku']

  if not any(key in string for key in ['frontend', 'front-end', 'css', 'sass', 'preprocessor', 'pre-processor']):
    ret.remove('CSS3/Sass')
  if not any(key in string for key in ['python', 'django', 'flask', 'numpy', 'machine learning']):
    ret.remove('Django')
  if 'express.js' in string:
    ret[ret.index('Node.js')] = 'Node/Express.js'

  ret = ret[:4]
  ret[-1] = 'and ' + ret[-1]

  return ', '.join(ret)

company = string[2][9:]
contact = string[len(string) - 3]
position = string[string.index('Position') + 1]
skills = get_skills(string)

cover_letter = """Dear %s,

My name is Catherine, and I am writing to apply to %s for a %s position. I am a web developer with experience across the stack using tools such as %s, and with these skills, I am confident I can add value to your team. If you are looking for a fast learner who loves to write clean, intuitive code, I could be a great fit for this role. 

As a developer, I believe in staying on top of the curve. By continuously honing my skills on fullstack projects, and keeping up with the latest frameworks and syntaxes, I am able to bring forth my best work at all times. Two of my recent projects include an online client for the popular card game Big 2, and a backend clone of Uber’s matching microservice API. These projects are available on github.com/kaaaata.

Thank you for your time and consideration, and I appreciate the chance to move forward!

Sincerely, 
Catherine Han""" % (contact, company, position, skills)

import os
os.system("echo '%s' | pbcopy" % cover_letter)
