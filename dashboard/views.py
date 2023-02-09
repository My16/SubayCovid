from argparse import OPTIONAL
from ssl import Options
from turtle import distance, position
from django.shortcuts import render
from folium.map import Marker, Popup
from .models import Dashboard, Data
import folium
from folium import LatLngPopup, plugins, raster_layers
from folium.plugins import MarkerCluster, LocateControl, MousePosition
from django_pandas.io import read_frame
from branca.element import Template, MacroElement
from django.core.paginator import Paginator

# Create your views here.
def dashboard(request):
    qs = Dashboard.objects.all()
    df_ = read_frame(qs, fieldnames=['cfname','total_covid_patients','discharged','conf_died'])

    sum_total_covid_patients = df_['total_covid_patients'].sum()
    sum_dischared = df_['discharged'].sum()
    sum_conf_died = df_['conf_died'].sum()

    for (index, rows) in df_.iterrows():
        cfname = rows.loc['cfname']
        total_covid_patients = rows.loc['total_covid_patients']
        discharged = rows.loc['discharged']
        conf_died = rows.loc['conf_died']

    context = {
        'qs':qs ,'sum_total_covid_patients': sum_total_covid_patients, 'sum_dischared': sum_dischared, 'sum_conf_died': sum_conf_died,
        'cfname': cfname, 'total_covid_patients': total_covid_patients, 'discharged': discharged, 'conf_died': conf_died
    }

    return render(request, 'dashboard.html', context)

def blank(request):
    # qs = Dashboard.objects.all()
    # df_ = read_frame(qs, fieldnames=['cfname','total_covid_patients','discharged','conf_died'])

    # sum_total_covid_patients = df_['total_covid_patients'].sum()
    # sum_dischared = df_['discharged'].sum()
    # sum_conf_died = df_['conf_died'].sum()

    # for (index, rows) in df_.iterrows():
    #     cfname = rows.loc['cfname']
    #     total_covid_patients = rows.loc['total_covid_patients']
    #     discharged = rows.loc['discharged']
    #     conf_died = rows.loc['conf_died']

    qs = Dashboard.objects.all()

    p = Paginator(Dashboard.objects.all(), 10)
    page = request.GET.get('page')
    p_qs = p.get_page(page)

    context = {
        # 'qs':qs ,'sum_total_covid_patients': sum_total_covid_patients, 'sum_dischared': sum_dischared, 'sum_conf_died': sum_conf_died,
        # 'cfname': cfname, 'total_covid_patients': total_covid_patients, 'discharged': discharged, 'conf_died': conf_died, 
        'qs':qs, 'p_qs':p_qs,
    }
    return render(request, 'blank.html', context)

def map(request):

    m = folium.Map(location=[12.8797, 121.7740], zoom_start=6)

    mc = MarkerCluster().add_to(m)

    map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter').add_to(m)
    map2 = raster_layers.TileLayer(tiles='CartoDB Positron').add_to(m)
    map3 = raster_layers.TileLayer(tiles='Stamen Terrain').add_to(m)
    map4 = raster_layers.TileLayer(tiles='Stamen Toner').add_to(m)
    map5 = raster_layers.TileLayer(tiles='Stamen Watercolor').add_to(m)

    folium.LayerControl().add_to(m)

    qs = Data.objects.all()
    df = read_frame(qs, fieldnames=['cfname', 'north_coord', 'east_coord', 'chances_patient_not_dying', 'total_ipcs', 
                    'ratio_patients_per_day_and_total_beds', 'ratio_staff_not_infected', 'ratio_total_staff_members', 'kmeans_label', 'Image', 'total_beds', 'tpatient_adm', 'total_staff_members', 'ambulance'])

    
    # Marker ang color
    for (index, rows) in df.iterrows():
        if rows.loc['kmeans_label'] == 0:
            iframe = folium.IFrame('Facility Name: ' + '<b>' + rows.loc['cfname'] + '</b>' + '<br>' + 'Details: ' + '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Beds:' + '<b>'  + '&nbsp;' + str(rows.loc['total_beds'])  + '</b>' + 
            '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Total Covid Patients:' + '<b>' + '&nbsp;' + str(rows.loc['tpatient_adm'])  + '</b>' + '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Staff Members:' + '<b>' + '&nbsp;' + str(rows.loc['total_staff_members'])  + '</b>' + 
            '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Ambulance:' + '<b>' + '&nbsp;' + str(rows.loc['ambulance'])  + '</b>' + '<br>' +'<img style="width:100%; height:100%;" src=' + rows.loc['Image'] + '>')
            popup = folium.Popup(iframe, min_width=500, max_width=500)
            folium.Marker(location=[rows.loc['north_coord'],
                                    rows.loc['east_coord']], popup=popup, tooltip=rows.loc['cfname'], icon=folium.Icon(color="blue")).add_to(mc)

        elif rows.loc['kmeans_label'] == 1:
            iframe = folium.IFrame('Facility Name: ' + '<b>' + rows.loc['cfname'] + '</b>' + '<br>' + 'Details: ' + '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Beds:' + '<b>'  + '&nbsp;' + str(rows.loc['total_beds'])  + '</b>' + 
            '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Total Covid Patients:' + '<b>' + '&nbsp;' + str(rows.loc['tpatient_adm'])  + '</b>' + '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Staff Members:' + '<b>' + '&nbsp;' + str(rows.loc['total_staff_members'])  + '</b>' + 
            '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Ambulance:' + '<b>' + '&nbsp;' + str(rows.loc['ambulance'])  + '</b>' + '<br>' +'<img style="width:100%; height:100%;" src=' + rows.loc['Image'] + '>')
            popup = folium.Popup(iframe, min_width=500, max_width=500)
            folium.Marker(location=[rows.loc['north_coord'],
                                    rows.loc['east_coord']], popup=popup, tooltip=rows.loc['cfname'], icon=folium.Icon(color="green")).add_to(mc)

        else:
            iframe = folium.IFrame('Facility Name: ' + '<b>' + rows.loc['cfname'] + '</b>' + '<br>' + 'Details: ' + '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Beds:' + '<b>'  + '&nbsp;' + str(rows.loc['total_beds'])  + '</b>' + 
            '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Total Covid Patients:' + '<b>' + '&nbsp;' + str(rows.loc['tpatient_adm'])  + '</b>' + '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Staff Members:' + '<b>' + '&nbsp;' + str(rows.loc['total_staff_members'])  + '</b>' + 
            '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Ambulance:' + '<b>' + '&nbsp;' + str(rows.loc['ambulance'])  + '</b>' + '<br>' +'<img style="width:100%; height:100%;" src=' + rows.loc['Image'] + '>')
            popup = folium.Popup(iframe, min_width=500, max_width=500)
            folium.Marker(location=[rows.loc['north_coord'],
                                    rows.loc['east_coord']], popup=popup, tooltip=rows.loc['cfname'], icon=folium.Icon(color="red")).add_to(mc)

        # elif rows.loc['kmeans_label'] == 3:
        #     iframe = folium.IFrame('Facility Name: ' + '<b>' + rows.loc['cfname'] + '</b>' + '<br>'+ '<img src="https://getwellhealthsystemsinc.com.ph/file-manager/images/Accredited%20Hospital/acebedo%20gen.jpg" alt="W3Schools.com" style="width:100%; height:75%;">')
        #     popup = folium.Popup(iframe, min_width=500, max_width=500)
        #     folium.Marker(location=[rows.loc['north_coord'],
        #                             rows.loc['east_coord']], popup=popup, tooltip=rows.loc['cfname'], icon=folium.Icon(color="orange")).add_to(mc)

        # else:
        #     iframe = folium.IFrame('Facility Name: ' + '<b>' + rows.loc['cfname'] + '</b>' + '<br>'+ '<img src="https://getwellhealthsystemsinc.com.ph/file-manager/images/Accredited%20Hospital/acebedo%20gen.jpg" alt="W3Schools.com" style="width:100%; height:75%;">')
        #     popup = folium.Popup(iframe, min_width=500, max_width=500)
        #     folium.Marker(location=[rows.loc['north_coord'],
        #                             rows.loc['east_coord']], popup=popup, tooltip=rows.loc['cfname'], icon=folium.Icon(color="pink")).add_to(mc)


        # elif rows.loc['kmeans_label'] == 1:
        #     iframe = folium.IFrame('FACILITY NAME: ' + rows.loc['cfname'] + '<br>' + 'TOTAL IPC: ' + str(rows.loc['total_ipcs']) + '<br>' + 
        #                             'PERCENTAGE OF STAFF NOT GETTING COVID: ' + str(rows.loc['Percentage_Staff_not_Covid']) + '<br>' + 'RATIO OF RECOVERED PATIENTS: ' + 
        #                             str(rows.loc['Ratio_Recovered_Patients']) + '<br>' + 'RATIO OF AMBULANCE PER PATIENTS: ' + str(rows.loc['Ratio_Ambulance_Patients']) + 
        #                             '<br>' + 'RATIO OF STAFF PER PATIENTS: ' + str(rows.loc['Ratio_Staff_Patients']))
        #     popup = folium.Popup(iframe, min_width=500, max_width=500)
        #     folium.Marker(location=[rows.loc['north_coord'],
        #                             rows.loc['east_coord']], popup=popup, tooltip=rows.loc['cfname'], icon=folium.Icon(color="green")).add_to(mc)

    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>jQuery UI Draggable - Default functionality</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    
    <script>
    $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

    </script>
    </head>
    <body>

    
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
        
    <div class='legend-title'>Clusters</div>
    <div class='legend-scale'>
    <ul class='legend-labels'>
        <li><span style='background:blue;opacity:0.7;'></span>Cluster 0</li>
        <li><span style='background:green;opacity:0.7;'></span>Cluster 1</li>
        <li><span style='background:red;opacity:0.7;'></span>Cluster 2</li>
        

    </ul>
    </div>
    </div>
    
    </body>
    </html>

    <style type='text/css'>
    .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
    .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
    .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
    .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
    .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
    .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""


    macro = MacroElement()
    macro._template = Template(template)

    m.get_root().add_child(macro)

    plugins.Fullscreen().add_to(m)
    LocateControl().add_to(m)
    MousePosition().add_to(m)

    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"

    MousePosition(
        position="bottomleft",
        separator=" | ",
        empty_string="NaN",
        lng_first=True,
        num_digits=20,
        prefix="Coordinates:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)
    
    m = m._repr_html_()

    context = {
        'm': m, 'qs': qs
    }

    return render(request, 'map.html', context)

def map_sample(request):
    m = folium.Map(location=[12.8797, 121.7740], zoom_start=6)

    mc = MarkerCluster().add_to(m)

    map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter').add_to(m)
    map2 = raster_layers.TileLayer(tiles='CartoDB Positron').add_to(m)
    map3 = raster_layers.TileLayer(tiles='Stamen Terrain').add_to(m)
    map4 = raster_layers.TileLayer(tiles='Stamen Toner').add_to(m)
    map5 = raster_layers.TileLayer(tiles='Stamen Watercolor').add_to(m)

    folium.LayerControl().add_to(m)


    qs = Data.objects.all()
    df = read_frame(qs, fieldnames=['cfname', 'north_coord', 'east_coord', 'chances_patient_not_dying', 'total_ipcs', 'ratio_patients_per_day_and_total_beds', 'ratio_staff_not_infected', 'ratio_total_staff_members', 'kmeans_label', 'Image', 'total_beds', 'tpatient_adm', 'total_staff_members', 'ambulance'])

    for (index, rows) in df.iterrows():
        if rows.loc['kmeans_label'] == 0:
            iframe = folium.IFrame('Facility Name: ' + '<b>' + rows.loc['cfname'] + '</b>' + '<br>' + 'Details: ' + '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Beds:' + '<b>'  + '&nbsp;' + str(rows.loc['total_beds'])  + '</b>' + 
            '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Total Covid Patients:' + '<b>' + '&nbsp;' + str(rows.loc['tpatient_adm'])  + '</b>' + '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Staff Members:' + '<b>' + '&nbsp;' + str(rows.loc['total_staff_members'])  + '</b>' + 
            '<br>' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + '&nbsp;' + 'Ambulance:' + '<b>' + '&nbsp;' + str(rows.loc['ambulance'])  + '</b>' + '<br>' +'<img style="width:100%; height:100%;" src=' + rows.loc['Image'] + '>')
            popup = folium.Popup(iframe, min_width=500, max_width=500)
            folium.Marker(location=[rows.loc['north_coord'],
                                    rows.loc['east_coord']], popup=popup, tooltip=rows.loc['cfname'], icon=folium.Icon(color="blue")).add_to(mc)
        elif rows.loc['kmeans_label'] == 1:
            folium.Marker(location=[rows.loc['north_coord'],
                                    rows.loc['east_coord']], tooltip=rows.loc['cfname'], icon=folium.Icon(color="green")).add_to(mc)
        else:
            folium.Marker(location=[rows.loc['north_coord'],
                                    rows.loc['east_coord']], tooltip=rows.loc['cfname'], icon=folium.Icon(color="red")).add_to(mc)


    m = m._repr_html_()

    context = {
        'm': m, 'qs':qs
    }
    return render(request, 'map_sample.html', context)

def about_us(request):
    return render(request, 'about-us.html', {})

def covisu(request):
    context = {}
    return render(request, 'covisu.html', context)

def gephi(request):
    context = {}
    return render(request, 'gephi.html', context)

def datamine(request):
    context = {}
    return render(request, 'datamine.html', context)