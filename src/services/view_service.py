from src.repositories.view_repository import ViewRepository
from src.json_encoder import rowToDict, resultToDict, rawResultsToDict
from functools import reduce

view_repository = ViewRepository()

class ViewService:
  def get_uncategorised_data(self, view, view_details):
    return {
      "title": view.title,
      "axisData": list(
        map(lambda col: {
            'xAxisTitle': view.x_axis,
            'xAxisValue': col[view.x_axis],
            'yAxisTitle': view.y_axis,
            'yAxisValue': col[view.y_axis]
          }, 
          view_details
        )
      )
    }
    
  def get_categorised_data(self, categories, view, view_details):
    x_axis_values = list(map(lambda detail: detail[view.x_axis], view_details))
    x_axis_values = sorted(set(x_axis_values), key=x_axis_values.index)
    
    data = {
      'xAxisTitle': view.x_axis,
      'xAxisValue': x_axis_values
    }
    
    filtered_view_details = []
    
    for value in x_axis_values:
      filtered = filter(lambda x: x[view.x_axis] == value, view_details)
      obj = []
      for element in filtered:
        obj.append({
          'yAxisTitle': element[view.categories],
          'yAxisValue': element[view.y_axis]
        })
      filtered_view_details.append(obj)
      
    data.update({'yAxisData': filtered_view_details})
  
    categories = rowToDict(view_repository.get_categories(view.name, categories))
    data.update({'categories': categories})
    data.update({'title': view.title})
    
    return data
  
  def inspect(self, id: str, from_date: str, to_date: str):
    view = view_repository.get_by_id(id)
    view_details = view_repository.inspect_view(id, from_date, to_date)
    
    if view:
      view = resultToDict(view)
    
    if len(view_details) > 0:
      view_details = rawResultsToDict(view_details)
      
    categories = view.categories
    
    if not categories:
      return self.get_uncategorised_data(view, view_details)
    
    return self.get_categorised_data(categories, view, view_details)
    
  def aggregate(self, view_id: str, from_date: str, to_date: str) -> dict:
    view = view_repository.get_by_id(int(view_id))
    view_details = view_repository.inspect_view(view_id, from_date, to_date)
    
    if len(view_details) == 0:
      raise Exception('No view details to aggregate')
      
    view = resultToDict(view)
    view_details = rawResultsToDict(view_details)
    
    method = view.aggregate
    x_axis = view.x_axis
    y_axis = view.y_axis
    title = view.title
    
    if not x_axis or not y_axis:
      raise Exception('False aggregate method for id=' + view_id)
    
    val_array = list(map(lambda elem: elem[y_axis], view_details))
    if method == 'sum':
      value = reduce(lambda a,b: a+b, val_array)
    elif method == 'count':
      value = len(val_array)
    elif method == 'avg':
      value = reduce(lambda a,b: a+b, val_array)/len(val_array)
    elif method == 'max':
      value = max(val_array)
    elif method == 'min':
      value = min(val_array)
    else:
      value = val_array[0]
    
    if method: 
      data = {
        'valueTitle': title if title else method + '_of_' + view.y_axis,
        'value': value,
        'aggregate': method
      }
    else:
      data = {
        'valueTitle': title if title else view.y_axis,
        'value': value
      }
      
    data.update({
      'x_axis': x_axis,
      'y_axis': y_axis,
    })
    
    return data