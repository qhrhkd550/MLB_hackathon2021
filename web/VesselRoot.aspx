<%@ Page Language="VB" AutoEventWireup="false" CodeFile="VesselRoot.aspx.vb" Inherits="_Default" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
        <div>


            <asp:Label ID="Label2" runat="server" Font-Bold="True" Font-Italic="False" Font-Size="Medium" Font-Underline="True" Text="2021 PNU AI·오픈소스SW 해커톤, Team MLB (빅데이터/AI기반 최적 추진효율 선박운항 기술 솔루션)"></asp:Label>
            <br />
            <br />
            <table style="width: auto;">
                <tr>
                    <td>
                        <asp:Label ID="Label1" runat="server" Text="선박고유번호(MMSI):"></asp:Label>
                    </td>
                    <td>
            <asp:RadioButtonList ID="RadioButtonList1" runat="server" AutoPostBack="True" DataSourceID="SqlDataSource1" DataTextField="MMSI" DataValueField="MMSI" RepeatColumns="10">
            </asp:RadioButtonList>
            <asp:SqlDataSource ID="SqlDataSource1" runat="server" ConnectionString="<%$ ConnectionStrings:ConnectionString %>" ProviderName="<%$ ConnectionStrings:ConnectionString.ProviderName %>" SelectCommand="select mmsi from data_hiems_ais_abstract group by mmsi order by mmsi"></asp:SqlDataSource>
                    </td>
                </tr>
            </table>
            <br />
            <asp:Label ID="Label4" runat="server" BackColor="Yellow" Font-Bold="True" Text="&lt;&lt; 선박 운항 정보 &gt;&gt;"></asp:Label>
            <br />
            <asp:GridView ID="GridView1" runat="server" AutoGenerateColumns="False" CellPadding="4" DataKeyNames="SHIP_ID,DETINATION_KEY" DataSourceID="SqlDataSource2" BackColor="White" BorderColor="#3366CC" BorderStyle="None" BorderWidth="1px" Font-Size="Medium">
                <Columns>
                    <asp:HyperLinkField DataNavigateUrlFields="lnk" DataTextField="DETINATION_KEY" HeaderText="항차" Target="GMAP" >
                    <ItemStyle HorizontalAlign="Right" />
                    </asp:HyperLinkField>
                    <asp:BoundField DataField="DESTINATION" HeaderText="Destination" SortExpression="DESTINATION" />
                    <asp:BoundField DataField="DRAUGHT" HeaderText="Draught" SortExpression="DRAUGHT" >
                    <ItemStyle HorizontalAlign="Right" />
                    </asp:BoundField>
                    <asp:BoundField DataField="DAYS" HeaderText="운항일" SortExpression="DAYS" >
                    <ItemStyle HorizontalAlign="Right" />
                    </asp:BoundField>
                    <asp:HyperLinkField DataNavigateUrlFields="DETINATION_KEY" DataNavigateUrlFormatString="http://localhost/MLB/MLBCharts.aspx?param=538008382_{0}" DataTextField="CNT" HeaderText="데이터 수" Target="MLBChart" >
                    <ItemStyle HorizontalAlign="Right" />
                    </asp:HyperLinkField>
                    <asp:BoundField DataField="DT_POS_UTC_FIRST_CHR" HeaderText="운항시작일시" SortExpression="DT_POS_UTC_FIRST_CHR" />
                    <asp:BoundField DataField="DT_POS_UTC_LAST_CHR" HeaderText="운항종료일시" SortExpression="DT_POS_UTC_LAST_CHR" />
                </Columns>
                <FooterStyle BackColor="#99CCCC" ForeColor="#003399" />
                <HeaderStyle BackColor="#003399" Font-Bold="True" ForeColor="#CCCCFF" />
                <PagerStyle BackColor="#99CCCC" ForeColor="#003399" HorizontalAlign="Left" />
                <RowStyle BackColor="White" ForeColor="#003399" />
                <SelectedRowStyle BackColor="#009999" Font-Bold="True" ForeColor="#CCFF99" />
                <SortedAscendingCellStyle BackColor="#EDF6F6" />
                <SortedAscendingHeaderStyle BackColor="#0D4AC4" />
                <SortedDescendingCellStyle BackColor="#D6DFDF" />
                <SortedDescendingHeaderStyle BackColor="#002876" />
            </asp:GridView>
            <asp:SqlDataSource ID="SqlDataSource2" runat="server" ConnectionString="<%$ ConnectionStrings:ConnectionString %>" ProviderName="<%$ ConnectionStrings:ConnectionString.ProviderName %>" SelectCommand="select A.*, 'http://localhost/MLB/AISpoly.html?psn='||mmsi||'_'||DETINATION_KEY lnk 
, decode(sign(draught_mean), 1, to_char(round(draught_mean, 1)), null) draught
, replace(DT_POS_UTC_FIRST,'202', '''2') DT_POS_UTC_FIRST_CHR
, replace(DT_POS_UTC_LAST,'202', '''2') DT_POS_UTC_LAST_CHR
from data_hiems_ais_abstract A
where mmsi=:Param1
order by DETINATION_KEY desc
">
                <SelectParameters>
                    <asp:ControlParameter ControlID="RadioButtonList1" DefaultValue="-1" Name="Param1" PropertyName="SelectedValue" />
                </SelectParameters>
            </asp:SqlDataSource>
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />


        </div>
    </form>
</body>
</html>
