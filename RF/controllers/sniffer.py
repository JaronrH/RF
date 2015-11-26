from components import featureBroker
from flask import render_template, request
from datetime import datetime
from sqlalchemy.sql.expression import desc
from entities import *
from datetime import datetime
import controllers
import json
from sqlalchemy import func
import app
from flask.ext.classy import FlaskView, route

class SnifferController(FlaskView):
    route_base = '/sniffer'

    @route('/')
    def index(self):
        """Renders the RF Sniffer log page."""
        return render_template(
            'sniffer.html',
            title='RF History',
            year=datetime.now().year
        )
    
    @route('/data')
    def data(self):
        """Retrieve data from DB for the Table"""
        results = {}   
    
        # Get Column Definitions
        columns = [
            None,
            RFSniffer.code,
            RFSniffer.date_created
        ]

        # Return Echo so that the DataTAble knows what to do!                                                                                        
        results['sEcho'] = request.args['sEcho']                                                                 

        # Get session
        session = app.db.session

        # Define what the query is over
        query = session.query(RFSniffer)
                         
        # Total Count                                                                          
        results['iTotalRecords'] = query.count()                                                                   

        # Filtered Count
        results['iTotalDisplayRecords'] =  results['iTotalRecords'] # TODO: Searching   

        # Ordering
        orderBy = columns[int(request.args['iSortCol_0'])]
        if (request.args['sSortDir_0'] == 'desc'):
            orderBy = desc(orderBy)

        records = query.order_by(orderBy).limit(int(request.args['iDisplayLength'])).offset(int(request.args['iDisplayStart']))
        
        # Data Output
        data = []                                  
        for record in records: 
            row = []
            
            row.append('<button data-code="'+str(record.code)+'" class="btn btn-primary btn-xs btn-lookupCode"><i class="fa fa-search fa-fw"></i></button>')
            row.append(record.code)
            row.append(controllers.Formatter.date(record.date_created))
                
            # Append Row                                                                                          
            data.append(row)                                                       

        # Assigned Data Output to Results
        results['aaData']=data  
                                                                                   
        return json.dumps(results)


featureBroker.features.Provide('controller', SnifferController)