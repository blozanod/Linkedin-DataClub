import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base, Session as SessionType
from sqlalchemy import and_

from Helper_Scripts.classes import Posting

# starting up the database 

postings_db = sa.create_engine(r"sqlite:///C:\Users\bfcla\Programming Projects\DataClub\Linkedin-DataClub\Backend\Databases\postings.db") # THIS WILL CHANGE BASED ON WINDOWS/MAC
Session = sessionmaker(bind=postings_db) # functions as the workspace
Base = declarative_base()

# sort dictionary that the function will index with an input string to get a Posting attribute to sort by
sort_dict = {
  "company_name": Posting.company_name,
  "title": Posting.title,
  "listed_time": Posting.listed_time,
  "salary": Posting.normalized_salary,
  "views": Posting.views,
  "applies": Posting.applies,
  "experience": Posting.formatted_experience_level
}

# Gets all of the postings
def get_all_postings(session: SessionType):
  """
  Gets every posting. Prob don't use this
  """
  return session.query(Posting).all()

# Uses keywords to search the job description and attaches any job that contains all keywords
def get_postings_by_keywords(session: SessionType, 
                             keywords: str = "",
                             sort_by:str = "company_name",
                             ascending: bool = True,
                             limit: int = 100):
  """
  Returns all resutls that contain the keywords
  """
  # create a list of filters containing a filter for each keyword 
  filters = [Posting.description.contains(keyword) for keyword in keywords.split()]  
  # construct a base query for the session with the filters 
  query = session.query(Posting).filter(and_(*filters)) 

  # executes sorting based on input string
  if sort_by in sort_dict:
    criteria = sort_dict[sort_by]
    query = query.filter(criteria.isnot(None)) # filter out the nonetype of chosen sort metric
    if ascending:
      result = query.order_by(criteria.asc()).limit(limit).all() # executes query here with the .all() method
    else:
      result = query.order_by(criteria.desc()).limit(limit).all()
  else:
    raise KeyError
  return result


def get_postings_by_title(session: SessionType, 
                          title_str: str = "",
                          sort_by:str = "company_name",
                          ascending: bool = True,
                          limit: int = 100):
  """
  Returns all results that contain the input string
  """
  query = session.query(Posting).filter(Posting.title.contains(title_str)) 

  if sort_by in sort_dict:
    criteria = sort_dict[sort_by]
    query = query.filter(criteria.isnot(None)) # filter out the nonetype of chosen sort metric
    if ascending:
      result = query.order_by(criteria.asc()).limit(limit).all() # executes query here with the .all() method
    else:
      result = query.order_by(criteria.desc()).limit(limit).all()
  else:
    raise KeyError
  
  return result

def get_postings_by_company_name(session: SessionType, 
                                 comp_str: str = "",
                                 sort_by:str = "company_name",
                                 ascending: bool = True,
                                 limit: int = 100):
  """
  Returns all results that contain the input string
  """
  query = session.query(Posting).filter(Posting.company_name.contains(comp_str))

  if sort_by in sort_dict:
    criteria = sort_dict[sort_by]
    query = query.filter(criteria.isnot(None)) # filter out the nonetype of chosen sort metric
    if ascending:
      result = query.order_by(criteria.asc()).limit(limit).all() # executes query here with the .all() method
    else:
      result = query.order_by(criteria.desc()).limit(limit).all()
  else:
    raise KeyError
  
  return result



def main() -> None:
  Base.metadata.create_all(postings_db)

  with Session.begin() as session:
    posting = session.query(Posting).first() # Basic test
    print(posting)

    sales_postings = get_postings_by_title(session,"Salesperson") # Testing get  postings by title
    print([posting.company_name for posting in sales_postings])



    company_postings = get_postings_by_company_name(session, "Pierce Refrigeration") # Testing get postings by company name
    print([posting.title for posting in company_postings])

    company_postings = get_postings_by_keywords(session, "software engineer") 
    print([posting.company_name for posting in company_postings])

    print([posting.title for posting in get_all_postings(session)])


  


if __name__ == "__main__":
  main()
