using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

// using 추가
using FusionCharts.Charts;
using System.Net;


public partial class MLBcharts : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        // 주소에서 ?param= 인자를 받아서 사용
        Chart_EngineRPM_Shipspeed(Request["param"]);
    }

    public void Chart_default()
    {
        //////////////////////////////////////
        // time series 차트 예시 임
        //////////////////////////////////////
        
        string schema, data;

        using (WebClient client = new WebClient())
        {
            //data = client.DownloadString("https://s3.eu-central-1.amazonaws.com/fusion.store/ft/data/plotting-multiple-series-on-time-axis-data.json");
            //schema = client.DownloadString("https://s3.eu-central-1.amazonaws.com/fusion.store/ft/schema/plotting-multiple-series-on-time-axis-schema.json");

            data = client.DownloadString("http://localhost/MLB/AIS_Chart_json/plotting-multiple-series-on-time-axis-data.json");
            schema = client.DownloadString("http://localhost/MLB/AIS_Chart_json/plotting-multiple-series-on-time-axis-schema.json");
        }

        FusionTable fusionTable = new FusionTable(schema, data);
        TimeSeries timeSeries = new TimeSeries(fusionTable);

        //timeSeries.AddAttribute('chart', @'{}');
        //timeSeries.AddAttribute('caption', @'{"text":"Sales Analysis"}');
        //timeSeries.AddAttribute('subcaption', @'{"text":"Grocery & Footwear"}');
        //timeSeries.AddAttribute('series', @'"Type"');
        //timeSeries.AddAttribute('yaxis', @'[{"plot":"Sales Value","title":"Sale Value","format":{"prefix":"$"}}]');

        // 위의 원본에서 "는 ""으로, '는 "으로 replace해야 한다.
        timeSeries.AddAttribute("chart", @"{}");
        timeSeries.AddAttribute("caption", @"{""text"":""Sales Analysis""}");
        timeSeries.AddAttribute("subcaption", @"{""text"":""Grocery & Footwear""}");
        timeSeries.AddAttribute("series", @"""Type""");
        timeSeries.AddAttribute("yaxis", @"[{""plot"":""Sales Value"",""title"":""Sale Value"",""format"":{""prefix"":""$""}}]");


        // charttype, chartID, width, height, data format, TimeSeries object
        Chart chart = new Chart("timeseries", "first_chart", "800", "550", "json", timeSeries);
        Literal1.Text = chart.Render();
    }

    public void Chart_EngineRPM_Shipspeed(string Param)
    {

        string schema, data;

        using (WebClient client = new WebClient())
        {
            data = client.DownloadString("http://localhost/MLB/ISS_json/" + Param + ".json");
            schema = client.DownloadString("http://localhost/MLB/ISS_json/MLB_schema.json");

            //////////////////////////////////////////////////////////
            // 한 축에 두개의 시리즈 그릴때
            //data = client.DownloadString("http://localhost/MLB/ISS_json/TypeChart.json");
            //schema = client.DownloadString("http://localhost/MLB/ISS_json/MLB_schema_Type_and_Speed_kmh.json");
            //////////////////////////////////////////////////////////
        }

        FusionTable fusionTable = new FusionTable(schema, data);
        TimeSeries timeSeries = new TimeSeries(fusionTable);

        timeSeries.AddAttribute("chart", @"{'multicanvas':false}"); //'multicanvas':false 있으면 한 chart에 두개 이상 축, 없으면 개별 chart로 나타남
        //timeSeries.AddAttribute("chart", @"{}");

        timeSeries.AddAttribute("caption", @"{""text"":""선박속력(km/h) & 엔진부하(%)""}");
        //timeSeries.AddAttribute("subcaption", @"{""text"":""Grocery & Footwear""}");
        //timeSeries.AddAttribute("series", @"""Type""");
        //timeSeries.AddAttribute("yaxis", @"[{""plot"":""Sales Value"",""title"":""Sale Value"",""format"":{""prefix"":""$""}}]");


        timeSeries.AddAttribute("xaxis", @"{'timemarker':[{'start':'2020-01-24 10:00', 'end':'2020-02-02 00:00', 'label':'FUEL SAVING AREA', 'timeFormat':'%Y-%m-%d %H:%M', type: 'full', 'style':{'marker':{'fill':'#f8b8b7'}}}]}");

        // 기본 (MLB_schema.json 에 있는 것을 써야 함)
        //timeSeries.AddAttribute("yaxis", @"[{'plot':[{'value':'Engine_RPM'}]}, {'plot':[{'value':'ShipSpeed_km/h'}]}]");
        //timeSeries.AddAttribute("yaxis", @"[{'plot':[{'value':'ShipSpeed_km/h'}], 'min':'0', 'max':'40'}, {'plot':[{'value':'OptSpeed_km/h'}], 'min':'0', 'max':'40', 'orientation': 'left'}, {'plot':[{'value':'EngineLoad_%'}], 'min':'0', 'orientation': 'right'}]");
        timeSeries.AddAttribute("yaxis", @"[{'plot':[{'value':'ShipSpeed(km/h)'}], 'min':'0', 'max':'40'}, {'plot':[{'value':'EngineLoad(%)'}], 'min':'0'}, {'plot':[{'value':'AI-Optimized ShipSpeed(km/h)'}], 'min':'0', 'max':'40'}]");

        // ShipSpeed_km/h 만
        //timeSeries.AddAttribute("yaxis", @"[{'plot':[{'value':'ShipSpeed_km/h'}]}]");

        // SOG까지 포함
        //timeSeries.AddAttribute("yaxis", @"[{'plot':[{'value':'Engine_RPM'}]}, {'plot':[{'value':'ShipSpeed_km/h'}]}, {'plot':[{'value':'SOG_km/h'}]}]");

        // OptSpeed_km/h까지 포함
        //timeSeries.AddAttribute("yaxis", @"[{'plot':[{'value':'Engine_RPM'}]}, {'plot':[{'value':'ShipSpeed_km/h'}]}, {'plot':[{'value':'OptSpeed_km/h'}]}]");
        //timeSeries.AddAttribute("yaxis", @"[{'plot':[{'value':'ShipSpeed_km/h'}]}, {'plot':[{'value':'OptSpeed_km/h'}]}]");

        //////////////////////////////////////////////////////////
        // 한 축에 두개의 시리즈 그릴때
        //timeSeries.AddAttribute("series", @"'Type'");
        //timeSeries.AddAttribute("yaxis", @"[{'plot':'Speed_km/h', 'title':'Speed (km/h)', 'min':'0'}]");
        //////////////////////////////////////////////////////////

        // charttype, chartID, width, height, data format, TimeSeries object
        Chart chart = new Chart("timeseries", "Literal2", "1102", "444", "json", timeSeries);
        Literal1.Text = chart.Render();
    }

}