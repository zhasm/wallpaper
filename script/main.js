function getResolution(){
	return screen.width+"x"+screen.height;
}

function urlDetailedToSpecific(url)
{
	//detail; http://interfacelift.com/wallpaper_beta/details/1543/falls.html
	//specifi: http://interfacelift.com/wallpaper_beta/grab/02432_eldtic_1680x1050.jpg
	var res=getResolution();
	var url=url.replace("/details/","/grab/");
	url=url.replace(/\/(\w+)\.html$/, "_$1_"+res+".jpg");
	return url;
}

function urlToImg(url){
		// 
		// =>
		// <a href=""><img src=""></a>
		// 
		//http://interfacelift.com/wallpaper_beta/previews/02424_skypainting.jpg
		//http://interfacelift.com/wallpaper_beta/details/1543/falls.html
		var ori=url;
	
		var url=url.replace("/previews/",'/details/');
		url=url.replace(/_(\w+)\.jpg$/,'/$1.html');
		return "<a href=\""+url+"\" title=\""+url+"\"><img class='wallpaper' src=\""+ori+"\"></a>";

	}

function setPageWallpaperNo(p,w)
{
	$("#s_page").html(p+" pages &amp;");
	$("#s_wallpapers").html(w+" images!");
	createCookie("s_page",p, 1);
}

function gotoPage(p)
{
	$("#images").html("<div><img src='image/ajax.gif' style='margin-top:20px; margin-bottom:20px;'></div>");
	
	createCookie("pageNo",p, 1);
	
	$.getJSON("http://zhasm.com/cgi-bin/api/iw.py?jsoncallback=?.json",
		{"page":p},
	 	function(data)
		{
		    //set tatal page number			
    		setPageWallpaperNo(data.pages, data.wallpapers);

    		imgs=data.imgs;
    		len=imgs.length;
    		result="";

    		for (i=0; i<len; i++)
    		{
    			result += urlToImg(imgs[i]);			
    		}

    		$("#images").html(result);

    		var bestFit=0;

    		//key press
    		$("*").keydown(
    			function(event)
    			{

    		        if(event.keyCode=='16')
    		        {	//16==shift, 17==control

    					bestFit=1;				
    		        }				

    		   	});//inner function ends

    		$("*").keyup(function(){
    			bestFit=0;
    		});

    		$("a").click(function(event){
    			url=$(this).attr("href");
    			if(bestFit ==1)
    		    {
    				url=urlDetailedToSpecific(url);	
    			}
    			chrome.tabs.create({'url': url});
    		}); //click ends

		});//get json ends
}
	
$(document).ready(function(){ 
	//begine	
	$("#b_Go").click(function(){
		p=$('#i_page').val();		
		gotoPage(p);
		
	});
	
	$("#latest").click(function(){
		
		p=1;
		$('#i_page').val(p);
		gotoPage(p);
					
	});
	
	$("#prev").click(function(){
		
		p=$('#i_page').val();
		p=parseInt(p);
		if (p>=2)
		{
			p -= 1;
			$('#i_page').val(p);
			gotoPage(p);
		}			
	});
	
	$("#next").click(function(){
		p=$('#i_page').val();
		p=parseInt(p);
		p+=1;
		$('#i_page').val(p);
		gotoPage(p);
	});
	
	$("#oldest").click(function(){
	    p=readCookie("s_page");
		$('#i_page').val(p);
		gotoPage(p);
	});
	
	var pageNo=readCookie("pageNo");
	if (!pageNo)
	{
	    pageNo=1;
	    createCookie("pageNo",pageNo, 1);
	}
	$('#i_page').val(pageNo);
	gotoPage(pageNo);			
	
	//end
});