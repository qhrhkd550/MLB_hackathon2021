<%@ Page Language="C#" AutoEventWireup="true" CodeFile="MLBcharts.aspx.cs" Inherits="MLBcharts" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title></title>
    <!-- Include fusioncharts core library -->
    <script type="text/javascript" src="https://cdn.fusioncharts.com/fusioncharts/latest/fusioncharts.js"></script>
    <!-- Include fusion theme -->
    <script type="text/javascript" src="https://cdn.fusioncharts.com/fusioncharts/latest/themes/fusioncharts.theme.fusion.js"></script>
</head>
<body>
    <form id="form1" runat="server">
        <div>
            <asp:Literal ID="Literal1" runat="server"></asp:Literal>
            <table style="width: auto; top: auto; clip: rect(auto, auto, auto, auto);">
                <tr>
                    <td style="vertical-align: top">
                        <asp:GridView ID="GridView1" runat="server" AutoGenerateColumns="False" BackColor="White" BorderColor="#999999" BorderStyle="Solid" BorderWidth="1px" CellPadding="3" DataSourceID="SqlDataSource1" GridLines="Vertical">
                            <AlternatingRowStyle BackColor="#DCDCDC" />
                            <Columns>
                                <asp:BoundField DataField="DT_POS_UTC_FIRST" HeaderText="시점" SortExpression="DT_POS_UTC_FIRST" />
                                <asp:BoundField DataField="DISTANCE_KM" HeaderText="운항거리" SortExpression="DISTANCE_KM" />
                                <asp:BoundField DataField="DURATION_CHR" HeaderText="운항기간" SortExpression="DURATION_CHR" />
                                <asp:BoundField DataField="SAVING_PCT" HeaderText="연료절감가능율" SortExpression="SAVING_PCT" >
                                <ItemStyle Font-Bold="True" Font-Italic="False" Font-Underline="True" HorizontalAlign="Center" />
                                </asp:BoundField>
                            </Columns>
                            <FooterStyle BackColor="#CCCCCC" ForeColor="Black" />
                            <HeaderStyle BackColor="#000084" Font-Bold="True" ForeColor="White" />
                            <PagerStyle BackColor="#999999" ForeColor="Black" HorizontalAlign="Center" />
                            <RowStyle BackColor="#EEEEEE" ForeColor="Black" />
                            <SelectedRowStyle BackColor="#008A8C" Font-Bold="True" ForeColor="White" />
                            <SortedAscendingCellStyle BackColor="#F1F1F1" />
                            <SortedAscendingHeaderStyle BackColor="#0000A9" />
                            <SortedDescendingCellStyle BackColor="#CAC9C9" />
                            <SortedDescendingHeaderStyle BackColor="#000065" />
                        </asp:GridView>
                        <asp:SqlDataSource ID="SqlDataSource1" runat="server" ConnectionString="<%$ ConnectionStrings:ConnectionString %>" ProviderName="<%$ ConnectionStrings:ConnectionString.ProviderName %>" SelectCommand="select * from VW_PUN_AIOPTIMIZED
where substr(:Param1, 0, 9)=mmsi
and substr(:Param1, 11)=caseno">
                            <SelectParameters>
                                <asp:QueryStringParameter DefaultValue="-1" Name="Param1" QueryStringField="param" />
                            </SelectParameters>
                        </asp:SqlDataSource>
                    </td>
                    <td>
                        <asp:GridView ID="GridView2" runat="server" AutoGenerateColumns="False" BackColor="White" BorderColor="#999999" BorderStyle="Solid" BorderWidth="1px" CellPadding="3" DataSourceID="SqlDataSource2" GridLines="Vertical">
                            <AlternatingRowStyle BackColor="#DCDCDC" />
                            <Columns>
                                <asp:BoundField DataField="SHIPSPEED_KM_H" HeaderText="최적운항모드:선박속력(km/h)" SortExpression="SHIPSPEED_KM_H" >
                                <ItemStyle HorizontalAlign="Center" />
                                </asp:BoundField>
                                <asp:BoundField DataField="ENGINELOAD_PCT" HeaderText="엔진부하(%)" SortExpression="ENGINELOAD_PCT">
                                <ItemStyle HorizontalAlign="Center" />
                                </asp:BoundField>
                                <asp:BoundField DataField="DIST_KM" HeaderText="운항거리(km)" SortExpression="DIST_KM">
                                <ItemStyle HorizontalAlign="Center" />
                                </asp:BoundField>
                                <asp:BoundField DataField="OPERATING_MIN" HeaderText="운항시간" SortExpression="OPERATING_MIN" >
                                <ItemStyle HorizontalAlign="Center" />
                                </asp:BoundField>
                            </Columns>
                            <FooterStyle BackColor="#CCCCCC" ForeColor="Black" />
                            <HeaderStyle BackColor="#000084" Font-Bold="True" ForeColor="White" />
                            <PagerStyle BackColor="#999999" ForeColor="Black" HorizontalAlign="Center" />
                            <RowStyle BackColor="#EEEEEE" ForeColor="Black" />
                            <SelectedRowStyle BackColor="#008A8C" Font-Bold="True" ForeColor="White" />
                            <SortedAscendingCellStyle BackColor="#F1F1F1" />
                            <SortedAscendingHeaderStyle BackColor="#0000A9" />
                            <SortedDescendingCellStyle BackColor="#CAC9C9" />
                            <SortedDescendingHeaderStyle BackColor="#000065" />
                        </asp:GridView>
                        <asp:SqlDataSource ID="SqlDataSource2" runat="server" ConnectionString="<%$ ConnectionStrings:ConnectionString %>" ProviderName="<%$ ConnectionStrings:ConnectionString.ProviderName %>" SelectCommand="select to_char(engineload_pct) engineload_pct
, round(shipspeed_km_h, 0) shipspeed_km_h
, to_char(round(distance_km, 1), 'FM9990.0') dist_km
,to_char(trunc(   (operating_min    /60)))||'시간 '
||to_char(round(mod(operating_min
, 60), 0))||'분' operating_min
from PNU_AIOPTIMIZED_PROFILE
where substr(:Param1, 0, 9)=mmsi
and substr(:Param1, 11)=caseno
order by engineload_pct desc">
                            <SelectParameters>
                                <asp:QueryStringParameter DefaultValue="-1" Name="Param1" QueryStringField="param" />
                            </SelectParameters>
                        </asp:SqlDataSource>
                    </td>
                </tr>
                <tr>
                    <td style="vertical-align: top">&nbsp;</td>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td style="vertical-align: top">&nbsp;</td>
                    <td>&nbsp;</td>
                </tr>
            </table>
            <br />
            <br />
            <br />
        </div>
    </form>
</body>
</html>
