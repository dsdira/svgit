from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('plantilla/', views.plantilla, name='plantilla'),
	path('add-wiki/<col>', views.addwiki, name='addwiki'),
	path('edit-wiki/<wikiid>', views.editwiki, name='editwiki'),
	path('wiki/<wid>', views.wiki, name='wiki'),
	path('', views.homepage, name='homepage'),
	path('add-book/', views.addbook, name='addbook'),
	path('book/<bookid>', views.book, name='book'),
	path('books/<y>', views.books, name='books'),
	path('bqueue/', views.bqueue, name='bqueue'),
	path('bunko/<y>', views.bunko, name='bunko'),
	path('bkqueue/', views.bkqueue, name='bkqueue'),
	path('readbook/', views.readbook, name='readbook'),
	path('appendwiki/', views.appendwiki, name='appendwiki'),
	path('page/<p>', views.pagina, name='page'),
	path('add-movie/', views.addmovie, name='addmovie'),
	path('movie/<movieid>', views.movie, name='movie'),
	path('watchmovie/', views.watchmovie, name='watchmovie'),
	path('movies/<y>', views.movies, name='movies'),
	path('mqueue/', views.mqueue, name='mqueue'),
	path('add-show/', views.addshow, name='addshow'),
	path('show/<show_id>', views.show, name='show'),
	path('watchshow/', views.watchshow, name='watchshow'),
	path('addnewseason/', views.addnewseason, name='addnewseason'),
	path('shows/', views.shows, name='shows'),
	path('showqueue/', views.showqueue, name='showqueue'),
	path('addnewrelwiki/', views.addnewrelwiki, name='addnewrelwiki'),
	path('itemcol/<itm>/<col>', views.itemcol, name='itemcol'),
	path('fastedit/', views.fastedit, name='fastedit'),
	path('addbooktolist/', views.addbooktolist, name='addbooktolist'),
	path('booklists/', views.booklists, name='booklists'),
	path('booklist/<lid>', views.booklist, name='booklist'),
	path('addprogressbar/', views.addprogressbar, name='addprogressbar'),
	path('saveprogress/', views.saveprogress, name='saveprogress'),
	path('statistics/', views.statistics, name='statistics'),
	path('search/', views.busqueda, name='search'),
	path('kindlePublish/<p>', views.htmlPublish, name='kindlePublish'),
	path('saveshowprogress/', views.saveshowprogress, name='saveshowprogress'),
	path('addbookmedia/', views.addbookmedia, name='addbookmedia'),
	path('addfilmmedia/', views.addfilmmedia, name='addfilmmedia'),
	path('savepost/', views.savepost, name='savepost'),
	path('journal/<y>', views.journal, name='journal'),
	path('addpersona', views.addpersona, name='addpersona'),
	path('mediastats', views.mediastats, name='mediastats'),
	path('addmoviecredits', views.addmoviecredits, name='addmoviecredits'),
	path('movieperson/<strPersona>', views.movieperson, name='movieperson'),
	path('bookduel/', views.bookduel, name='bookduel'),
	path('savebookduel/<l>/<r>/<w>', views.savebookduel, name='savebookduel'),
	path('movieduel/', views.movieduel, name='movieduel'),
	path('savemovieduel/<l>/<r>/<w>', views.savemovieduel, name='savemovieduel'),
	path('quemarlibro/<libro>', views.quemarlibro, name='quemarlibro'),
	path('getmovie/', views.moviedbImport, name='moviedbImport'),
	path('savemovie/', views.savemovie, name='savemovie'),
	path('addtimesmedia/', views.addtimesmedia, name='addtimesmedia'),
	path('mediapage/<p>', views.mediapage, name='mediapage'),
	path('addbooktags/', views.addbooktags, name='addbooktags'),
	path('booktag/<this_tag>', views.viewbooktag, name='viewbooktag'),
	path('addbookquote/', views.addbookquote, name='addbookquote'),
	path('addmovietolist/', views.addmovietolist, name='addmovietolist'),
	path('movielists/', views.movielists, name='movielists'),
	path('movielist/<id_lista>', views.movielist, name='movielist'),

	path('addwikiphoto/', views.addwikiphoto, name='addwikiphoto'),
	path('cuadernos/', views.cuadernos, name='cuadernos'),
	path('addcuaderno/', views.addcuaderno, name='addcuaderno'),
	path('cuaderno/<c>', views.cuaderno, name='cuaderno'),
	path('printed-nb/<c>', views.nbtokindle, name='printedNB'),
	path('addapunte/', views.addapunte, name='addapunte'),
	path('editapunte/<aid>', views.editapunte, name='editapunte'),
	path('addmatch/<lid>/', views.addPartido, name='addmatch'),
	path('add-soccer-team/',views.addSoccerTeam,name='addSoccerTeam'),
	path('team/<t>', views.sccteam, name='sccteam'),
	path('viewmatch/<pid>/', views.viewMatch, name='viewmatch'),
	path('viewliga/<sta>/<lig>', views.viewLiga, name='viewliga'),
	path('closematch/<pid>/', views.closeMatch, name='closematch'),
	path('editmatch/<pid>/', views.editPartido, name='editmatch'),
	path('newplayergoal/<t>/<m>/<a>/', views.addNewPlayerGoal, name='newplayergoal'),
	path('regpenround/<pid>', views.regPenRound, name='regpenround'),
	path('addplayerv2/', views.addPlayerv2, name='addplayerv2'),
	path('addpartidocomm/',views.addpartidocomm,name="addpartidocomm"),
	path('addsecleg/', views.addsecleg, name='addsecleg'),
	path('squad/<par_id>/<equ_id>', views.viewsquad, name='viewsquad'),
	path('viewmatches/<sta>/', views.viewMatches, name='viewmatches'),
	path('jugadores/', views.jugadores, name='jugadores'),
	path('view-table/<liga>',views.viewTable,name='viewTable'),
	path('unirligateams/<liga>', views.unirligateams, name='unirligateams'),
	path('edit-comm/<commid>/', views.editComm, name='editComm'),
	path('jugador/<jid>', views.jugador, name='jugador'),
	path('view-contrato/<c>',views.editContrato,name='editContrato'),
	path('updatesquad/', views.updateSquad, name='updatesquad'),
	path('edit-bio/<c>',views.editBiographics,name='editBio'),
	path('finance/', views.finance, name='finance'),
	path('financemob/', views.finance2, name='finance2'),
	path('savetrx/', views.saveTrx, name='savetrx'),
	path('savepmt/', views.savePmt, name='savepmt'),
	path('addbudget/',views.addBudgetReg,name='addBudget'),
	path('view-month/<y>/<m>', views.viewmonth, name='viewmonth'),
	path('addapucon/',views.addapucon,name='addapucon'),
	path('vphoto/<photo>/<pagina>',views.mphoto,name='photo'),
	path('etiqueta/<y>/<e>',views.etiqueta,name='etiqueta'),

	]