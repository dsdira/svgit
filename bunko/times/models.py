from django.db import models
from datetime import datetime
from datetime import date
from django.db import models
from django.utils import timezone
import os
from uuid import uuid4
from django.db.models import Q, Avg, Count, Min, Sum
from random import choice
from django.utils.timezone import now
import re
import markdown

def path_and_name(instance, filename):
    upload_to = 'wiki_media'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class WikiType(models.Model):
	category = models.CharField(max_length=255)

	def __str__(self):
		return self.category

class Wiki(models.Model):
	wtype = models.ForeignKey(WikiType,on_delete=models.CASCADE)
	title = models.CharField(max_length=512)
	info = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(null=True,blank=True)

	def __str__(self):
		return self.title

	@property
	def headtext(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			return self.info[0:350]
		else:
			return self.info[0:n_corte]

	@property
	def cleantext(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			return self.info
		else:
			return self.info.replace('==headtext==','')

	@property
	def fecha_c(self):
		return self.updated_at.strftime("%Y-%m-%d")

	@property
	def mainPic(self):
		npics = WikiPhoto.objects.filter(wiki__id=self.id,imgtype=1).count()
		if npics == 0:
			return None
		else:
			pks = WikiPhoto.objects.filter(wiki=self.id,imgtype=1).values_list('pk', flat=True)
			random_pk = choice(pks)
			ppic = WikiPhoto.objects.get(pk=random_pk)
			return ppic.imagen.url
	@property
	def mdOutput(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			this_texto = self.info
		else:
			this_texto = self.info.replace('==headtext==','')
		return(markdown.markdown(this_texto,extensions=['extra']))

	@property
	def onbookcomm(self):
		conteo = MediaWiki.objects.filter(media_type=1,mwiki=self).count()

		if conteo == 0:
			return ""
		else:
			this_mediawiki = MediaWiki.objects.filter(media_type=1,mwiki=self).latest('id')
			this_book = Book.objects.get(pk=int(this_mediawiki.media_id))
			return " on <a href='/book/" + str(this_book.id) + "' style='text-decoration:none;'>"+this_book.titulo+"</a> "
	@property
	def nbooks(self):
		conteo = Credito.objects.filter(ctype__id=1,media_type=1,persona=self).count()
		return conteo

	@property
	def readbooks(self):
		conteo_all = Credito.objects.filter(ctype__id=1,media_type=1,persona=self).count()
		if conteo_all > 0:
			pks = Credito.objects.filter(ctype__id=1,media_type=1,persona=self).values_list('media_id', flat=True)
			distinct_count = Consumo.objects.filter(volume__id__in=pks,finish_d__isnull=False).values('volume__id').annotate(count=Count('volume__id', distinct=True)).count()
			return distinct_count
		else:
			return 0

		


class Book(models.Model):
	title = models.CharField(max_length=512)
	orig_lan = models.CharField(max_length=2)
	info = models.TextField()
	pub_year = models.IntegerField()
	wtype = models.ForeignKey(WikiType,on_delete=models.CASCADE)

	def __str__(self):
		return self.title+' ('+ str(self.pub_year) +')'

	@property
	def headtext(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			return self.info[0:350]
		else:
			return self.info[0:n_corte]

	@property
	def cleantext(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			return self.info
		else:
			return self.info.replace('==headtext==','')

	@property
	def titulo(self):
		return self.title+' ('+ str(self.pub_year) +')'

	@property
	def authors_links(self):
		creds = Credito.objects.filter(ctype__id__in=[1,5,6,7],media_type=1,media_id=self.id)

		enlaces = ""

		for c in creds:
			enlaces = enlaces + "<a href='/wiki/"+str(c.persona.id)+"' style='text-decoration:none; color:#6F8FAF;'>"+c.persona.title+"</a>,&nbsp;"

		return enlaces[:-7]

	@property
	def rhist(self):
		conteo = Consumo.objects.filter(volume__id=self.id).count()
		if conteo == 0:
			rcheck = 0
		else:
			rcheck = 1
		return rcheck

	@property
	def last_read(self):
		conteo = Consumo.objects.filter(volume__id=self.id).count()
		if conteo == 0:
			rcheck = None
		else:
		    robject = Consumo.objects.filter(volume__id=self.id).latest('-finish_d')
		    rcheck = robject.finish_d
		return rcheck

	@property
	def mainPic(self):
		npics = BookMedia.objects.filter(libro__id=self.id,imgtype=1).count()
		if npics == 0:
			return None
		else:
			pks = BookMedia.objects.filter(libro__id=self.id,imgtype=1).values_list('pk', flat=True)
			random_pk = choice(pks)
			ppic = BookMedia.objects.get(pk=random_pk)
			return ppic.imagen.url

	@property
	def legacyRead(self):
		return RelBookList.objects.filter(bbook__id=self.id,blist__id=28).count()




class CreditType(models.Model):
	credit_type = models.CharField(max_length=255)
	def __str__(self):
		return self.credit_type

class Credito(models.Model):
	ctype = models.ForeignKey(CreditType,on_delete=models.CASCADE)
	persona = models.ForeignKey(Wiki,on_delete=models.CASCADE)
	media_type = models.IntegerField()
	media_id = models.IntegerField()

	def __str__(self):
		return self.persona.title +' @ '+ self.ctype.credit_type

class Movie(models.Model):
	title = models.CharField(max_length=512)
	info = models.TextField()
	premiere = models.IntegerField()
	runtime = models.IntegerField()

	def __str__(self):
		return self.title+' ('+ str(self.premiere) +')'

	@property
	def titulo(self):
		return self.title+' ('+ str(self.premiere) +')'
	@property
	def headtext(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			return self.info[0:350]
		else:
			return self.info[0:n_corte]

	@property
	def cleantext(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			return self.info
		else:
			return self.info.replace('==headtext==','')

	@property
	def mainPic(self):
		npics = MovieMedia.objects.filter(film__id=self.id,imgtype=1).count()
		if npics == 0:
			return None
		else:
			pks = MovieMedia.objects.filter(film__id=self.id,imgtype=1).values_list('pk', flat=True)
			random_pk = choice(pks)
			ppic = MovieMedia.objects.get(pk=random_pk)
			return ppic.imagen.url

	@property
	def last_watch(self):
		conteo = MovieWatch.objects.filter(film__id=self.id).count()
		if conteo == 0:
			rcheck = None
		else:
		    robject = MovieWatch.objects.filter(film__id=self.id).latest('-wdate')
		    rcheck = robject.wdate
		return conteo


class Show(models.Model):
	title = models.CharField(max_length=512)
	info = models.TextField()
	wtype = models.ForeignKey(WikiType,on_delete=models.CASCADE)
	def __str__(self):
		return self.title

	@property
	def headtext(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			return self.info[0:350]
		else:
			return self.info[0:n_corte]

	@property
	def cleantext(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			return self.info
		else:
			return self.info.replace('==headtext==','')
	@property
	def consumos(self):
		ncons = ShowWatch.objects.filter(sseason__show__id=self.id).count()

		return ncons

	@property
	def transmision(self):
		premiers = Season.objects.filter(show=self).values_list('premiere',flat=True)

		max_p = max(premiers)
		min_p = min(premiers)

		if max_p == min_p:
			str_t = str(max_p)
		else:
			str_t = str(min_p)+'-'+str(max_p)

		return str_t

	@property
	def conteo_s(self):
		n_seasons = Season.objects.filter(show__id = self.id).count()

		return n_seasons


class Season(models.Model):
	show = models.ForeignKey(Show,on_delete=models.CASCADE)
	season_t = models.CharField(max_length=255, null=True, blank=True)
	info = models.TextField()
	episodes = models.IntegerField()
	avg_runtime = models.IntegerField()
	premiere = models.IntegerField()

	def __str__(self):
		return self.show.title+' '+self.season_t+' ('+ str(self.premiere) +')'

	@property
	def titulo(self):
		if len(self.season_t)<=3:
			return self.show.title+' '+self.season_t+' ('+ str(self.premiere) +')'
		else:
			return self.season_t+' ('+ str(self.premiere) +')'
	@property
	def headtext(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			return self.info[0:350]
		else:
			return self.info[0:n_corte]

	@property
	def cleantext(self):
		n_corte = self.info.find('==headtext==')
		if n_corte == -1:
			return self.info
		else:
			return self.info.replace('==headtext==','')

	@property
	def consumos(self):
		n_cons = ShowWatch.objects.filter(sseason__id = self.id).count()

		return n_cons

	@property
	def barras(self):
		n_barras = SeasonProgressBar.objects.filter(temporada=self, avance__lt=self.episodes).count()

		return n_barras

	@property
	def actual_barras(self):
		n_barras = SeasonProgressBar.objects.filter(temporada=self, avance__lt=self.episodes).count()

		if n_barras > 0:
			this_barras = SeasonProgressBar.objects.filter(temporada=self, avance__lt=self.episodes)
			return this_barras
		else:
			return None

class Consumo(models.Model):
	volume = models.ForeignKey(Book,on_delete=models.CASCADE)
	pages = models.IntegerField()
	start_d = models.DateField()
	finish_d = models.DateField()



	def __str__(self):
		return self.volume.titulo

class Pagina(models.Model):
	titulo = models.CharField(max_length=255)
	info = models.TextField()
	def __str__(self):
		return self.titulo

class PageRels(models.Model):
	page = models.ForeignKey(Pagina, on_delete=models.CASCADE)
	child = models.ForeignKey(Wiki,on_delete=models.CASCADE)

	def __str__(self):
		return self.page.titulo

class MovieWatch(models.Model):
	film = models.ForeignKey(Movie, on_delete=models.CASCADE)
	wdate = models.DateField()

	def __str__(self):
		return self.film.titulo

class ShowWatch(models.Model):
	sseason = models.ForeignKey(Season,on_delete=models.CASCADE)
	start_d = models.DateField()
	finish_d = models.DateField()

	def __str__(self):
		return self.sseason.show.title+' '+self.sseason.season_t

class MediaWiki(models.Model):
	mwiki = models.ForeignKey(Wiki, on_delete=models.CASCADE)
	media_type = models.IntegerField()
	media_id = models.IntegerField()

	def __str__(self):
		return self.mwiki.title

class BookList(models.Model):
	listname = models.CharField(max_length=500)
	date_created = models.DateField(auto_now=True)
	listinfo = models.TextField()
	tipo = models.IntegerField(default=0)

	def __str__(self):
		return self.listname

	@property
	def conteo(self):
		cont = RelBookList.objects.filter(blist=self).count()

		return cont

	@property
	def lecturas(self):
		n_lecturas = RelBookList.objects.filter(blist=self, bbook__consumo__finish_d__gt=self.date_created).count()
		return n_lecturas


class RelBookList(models.Model):
	blist = models.ForeignKey(BookList,on_delete=models.CASCADE)
	bbook =models.ForeignKey(Book,on_delete=models.CASCADE)

	def __str__(self):
		return self.blist.listname+' - '+self.bbook.titulo

class ProgressBar(models.Model):
	libro = models.ForeignKey(Book,on_delete=models.CASCADE)
	units = models.CharField(max_length=50)
	cantidad = models.IntegerField()
	avance = models.IntegerField(blank=True,default=0)
	fecha_inicio = models.DateField()


	def __str__(self):
		return self.libro.titulo

	@property
	def prct_prog(self):
		return round(self.avance/self.cantidad*100.00,2)


class ProgressLog(models.Model):
	barra = models.ForeignKey(ProgressBar,on_delete=models.CASCADE)
	fecha = models.DateField()
	progreso = models.IntegerField()
	delta_lec = models.IntegerField(default=0)

	def __str__(self):
		return str(self.id)+'-'+self.barra.libro.titulo


class SeasonProgressBar(models.Model):
	temporada = models.ForeignKey(Season, on_delete=models.CASCADE)
	avance = models.IntegerField(blank=True,default=0)
	fecha_inicio = models.DateField()

	def __str__(self):
		return self.temporada.titulo

	@property
	def prct_prog(self):
		return round(self.avance/self.temporada.episodes*100.00,2)

class SeasonProgressLog(models.Model):
	barra = models.ForeignKey(SeasonProgressBar,on_delete=models.CASCADE)
	fecha = models.DateField()
	progreso = models.IntegerField()
	delta_lec = models.IntegerField(default=0)

	def __str__(self):
		return str(self.id)+'-'+self.barra.temporada.titulo

class BookMedia(models.Model):
	libro = models.ForeignKey(Book,on_delete=models.CASCADE)
	imgtype = models.IntegerField()
	imagen = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)

	def __str__(self):
		return self.libro.titulo

class MovieMedia(models.Model):
	film = models.ForeignKey(Movie,on_delete=models.CASCADE)
	imgtype = models.IntegerField()
	imagen = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)

	def __str__(self):
		return self.film.titulo

class ItemMedia(models.Model):
	item = models.ForeignKey(Wiki,on_delete=models.CASCADE)
	imgtype = models.IntegerField()
	imagen = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)

	def __str__(self):
		return self.item.title

class MovieCredit(models.Model):
	film = models.ForeignKey(Movie,on_delete=models.CASCADE)
	credit = models.CharField(max_length=200)
	persona = models.CharField(max_length=200)
	def __str__(self):
		return self.persona+' @ '+ self.film.titulo

class BookDuel(models.Model):
	left_b = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='left_b')
	right_b = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='right_b')
	win_b = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='win_b')

	def __str__(self):
		return self.left_b.titulo+' @ '+ self.right_b.titulo


class MovieDuel(models.Model):
	left_b = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='left_b')
	right_b = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='right_b')
	win_b = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='win_b')

	def __str__(self):
		return self.left_b.titulo+' @ '+ self.right_b.titulo


class TimesMedia(models.Model):
	title = models.CharField(max_length=512)
	imgtype = models.IntegerField()
	imagen = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)
	created_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class BookTag(models.Model):
	libro = models.ForeignKey(Book, on_delete=models.CASCADE)
	tag = models.CharField(max_length=256)

	def __str__(self):
		return self.tag

class BookQuote(models.Model):
	libro = models.ForeignKey(Book, on_delete=models.CASCADE)
	quote = models.TextField()

	def __str__(self):
		return str(self.id)+'-'+self.quote[0:50]

class MovieList(models.Model):
	titulo = models.CharField(max_length=512)
	created_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.titulo

	@property
	def conteo(self):
		cont = MoveListItem.objects.filter(lista__id=self.id).count()
		return cont

class MoveListItem(models.Model):
	lista = models.ForeignKey(MovieList, on_delete = models.CASCADE)
	film = models.ForeignKey(Movie, on_delete = models.CASCADE)

	def __str__(self):
		return self.lista.titulo +  '@' + self.film.titulo

class WikiPhoto(models.Model):
	wiki = models.ForeignKey(Wiki,on_delete=models.CASCADE)
	imgtype = models.IntegerField()
	imagen = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)

	def __str__(self):
		return self.wiki.title

class Cuaderno(models.Model):
	titulo = models.CharField(max_length=200)
	fecha_creacion = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.titulo

class Apunte(models.Model):
	cuaderno = models.ForeignKey(Cuaderno, on_delete=models.CASCADE)
	contenido = models.TextField()
	fecha_creacion = models.DateTimeField(auto_now=True)
	subtitulo = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.cuaderno.titulo


	@property
	def parrafoeditable(self):
		return self.contenido +' '+ f"<a href='/editapunte/{self.id}' style='color:gray; font-size: 0.85em;'>[ed]</a>"

	@property
	def consumos(self):
		n_cons = ApunteConsumo.objects.filter(apunte__id = self.id).count()

		return n_cons


class Equipo(models.Model):
	nombre = models.CharField(max_length=128)
	pais = models.CharField(max_length=128)
	logo = models.ImageField(upload_to=path_and_name, max_length=255, null=True, blank=True)

	def __str__(self):
		return self.nombre

class Jugador(models.Model):
	nombre = models.CharField(max_length=128)
	pais = models.CharField(max_length=128)
	biographics = models.TextField(default="This section needs to be expanded.")

	def __str__(self):
		return self.nombre

class Contrato(models.Model):
	jug = models.ForeignKey(Jugador, on_delete = models.CASCADE)
	equ = models.ForeignKey(Equipo, on_delete = models.CASCADE)
	active = models.BooleanField(default=True)
	position = models.CharField(default="Not Specified", max_length=256)
	number = models.IntegerField(default = 0)

	def __str__(self):
		return self.jug.nombre+'-'+self.equ.nombre

class Liga(models.Model):
	nombre = models.CharField(max_length=120)

	def __str__(self):
		return self.nombre


class Partido(models.Model):
	fecha = models.DateField()
	liga = models.ForeignKey(Liga, on_delete = models.CASCADE)
	local = models.ForeignKey(Equipo, on_delete = models.CASCADE,related_name="elocal")
	visita = models.ForeignKey(Equipo, on_delete = models.CASCADE,related_name="evisita")
	terminado = models.BooleanField(default=False, blank=True,null=True)
	fase = models.CharField(max_length=120)

	def __str__(self):
		return self.local.nombre+' v '+self.visita.nombre

	@property
	def marcador(self):
		nlocal = Goles.objects.filter(partido__id=self.id,asignado=1,penales=False).count()
		nvisita = Goles.objects.filter(partido__id=self.id,asignado=2,penales=False).count()

		plocal = Goles.objects.filter(partido__id=self.id,asignado=1,penales=True).count()
		pvisita = Goles.objects.filter(partido__id=self.id,asignado=2,penales=True).count()

		if (plocal+pvisita)==0:
			score = "{} - {}".format(nlocal,nvisita)
		else:
			score = "{} ({})-({}) {}".format(nlocal,plocal,pvisita,nvisita)

		return score

	@property
	def comms(self):
		comentarios = PartidoComment.objects.filter(comm_partido__id=self.id)
		txt_comms = ""
		if comentarios:
			for c in comentarios:
				txt_comms = txt_comms +' '+ c.comm

			return txt_comms
		else:
			return None




class Goles(models.Model):
	partido = models.ForeignKey(Partido,on_delete=models.CASCADE)
	asignado = models.IntegerField()
	contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
	minuto = models.IntegerField()
	adicional = models.IntegerField()
	penal = models.BooleanField()
	penales = models.BooleanField()
	og = models.BooleanField(default=False)

	def __str__(self):
		return self.contrato.jug.nombre

	@property
	def descriptor(self):

		if self.adicional>0:
			add = "+"+str(self.adicional)
		else:
			add = ""

		if self.penal:
			p = " pen"
		else:
			p = ""

		if self.og:
			fog = " og"
		else:
			fog =""

		desc = self.contrato.jug.nombre+" "+str(self.minuto)+"'"+add+p+fog

		return desc

class Penales(models.Model):
	partido = models.ForeignKey(Partido,on_delete=models.CASCADE)
	asignado = models.IntegerField()
	contrato = models.ForeignKey(Contrato,on_delete=models.CASCADE)
	anotado = models.BooleanField()

	def __str__(self):
		return str(self.id)

	@property
	def icon(self):
		if self.anotado == True:
			symbol = "&#9989;"
		else:
			symbol = "&#10060;"

		return symbol

class PartidoComment(models.Model):
	comm_partido = models.ForeignKey(Partido,on_delete=models.CASCADE)
	comm = models.TextField()
	minuto  = models.IntegerField(default=0)
	tipo = models.IntegerField(default=0)

	def __str__(self):
		return str(self.id)

class LigaTeams(models.Model):
    ligaRel = models.ForeignKey(Liga,on_delete = models.CASCADE)
    equipoRel = models.ForeignKey(Equipo,on_delete = models.CASCADE)
    flagActivo = models.BooleanField(default=True)

    def __str__(self):
        return self.ligaRel.nombre+'-'+self.equipoRel.nombre

class mlbTeam(models.Model):
	nombre = models.CharField(max_length=200)
	ciudad = models.CharField(max_length=200)
	nomina = models.TextField()

	def __str__(self):
		return self.nombre


class mlbGame(models.Model):
	fecha = models.DateField()
	local = models.ForeignKey(mlbTeam,on_delete=models.CASCADE, related_name='local_team')
	visit = models.ForeignKey(mlbTeam,on_delete=models.CASCADE, related_name='visit_team')
	local_runs = models.IntegerField()
	visit_runa = models.IntegerField()
	comentarios = models.TextField()

	def __str__(self):
		return str(self.id)+" | "+self.local.nombre +" v "+self.visit.nombre

class matchSquad(models.Model):
	partido = models.ForeignKey(Partido,on_delete=models.CASCADE)
	equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)

	def __str__(self):
		return "partido: " + str(self.partido.id) + " - "+ self.equipo.nombre

class squadPlayers(models.Model):
	squad = models.ForeignKey(matchSquad,on_delete=models.CASCADE)
	jugador = models.ForeignKey(Contrato,on_delete=models.CASCADE)
	tipo = models.CharField(max_length=1)

	def __str__(self):
		return "partido: " + str(self.squad.partido.id) + " - "+ self.jugador.jug.nombre

class Cuenta(models.Model):
	nombre = models.CharField(max_length=150)
	tipo = models.IntegerField()

	def __str__(self):
		return self.nombre

class TrxTyp(models.Model):
	desc = models.CharField(max_length=200)
	codigo = models.IntegerField()

	def __str__(self):
		return self.desc

class Trx(models.Model):
	fecha = models.DateField()
	debito = models.ForeignKey(Cuenta, on_delete = models.CASCADE)
	credito = models.ForeignKey(TrxTyp, on_delete = models.CASCADE)
	monto = models.DecimalField(max_digits=16,decimal_places=2,default=0.00)
	desc = models.CharField(max_length=200)

	def __str__(self):
		return self.credito.desc +'--'+ str(self.fecha)


class Budget(models.Model):
	cuenta = models.ForeignKey(TrxTyp,on_delete=models.CASCADE)
	anho = models.IntegerField()
	mes = models.IntegerField()
	mbudget = models.DecimalField(max_digits=16,decimal_places=2,default=0.00)

	def __str__(self):
		return str(self.anho)+'-'+str(self.mes)+':'+self.cuenta.desc

class ApunteConsumo(models.Model):
	apunte = models.ForeignKey(Apunte,on_delete=models.CASCADE)
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField(blank=True,null=True)
	media_type = models.CharField(max_length=100)
	unidades = models.CharField(max_length=100)
	cantidad = models.IntegerField()



	def __str__(self):
		return self.apunte.subtitulo

class Tweet(models.Model):
	texto = models.TextField()
	updated_at = models.DateTimeField(auto_now=True,editable=False)
	created_at = models.DateField(default=date.today)

	@property
	def cleantext(self):
		pat = re.compile(r"#(\w+)")
		listado = pat.findall(self.texto)

		this_text = self.texto

		if len(listado)>0:
			for l in listado:
				this_text = this_text.replace("#"+l,"")

		return this_text.strip()

	@property
	def hashtags(self):
		pat = re.compile(r"#(\w+)")
		listado = pat.findall(self.texto)

		this_tags = ''

		if len(listado)>0:
			for l in listado:
				this_tags = this_tags + "<a href='/etiqueta/1/{}' style='text-decoration:none;'>#{}</a> ".format(l,l)

		return this_tags


	def __str__(self):
		return self.texto[0:40]

class Etiqueta(models.Model):
	tweet = models.ForeignKey(Tweet, on_delete = models.CASCADE)
	etiqueta = models.CharField(max_length=100)

	def __str__(self):
		return self.etiqueta

class BookEntity(models.Model):
	libro = models.ForeignKey(Book,on_delete=models.CASCADE)
	etype = models.CharField(max_length=50)
	nombre = models.CharField(max_length=250)
	info = models.TextField()
	importancia = models.IntegerField(default=50)

	def __str__(self):
		return self.nombre

	@property
	def afiliations(self):
		texto_grupos = ""
		grupos = BookGroupEntity.objects.filter(entity=self)
		if grupos:
			for g in grupos:
				texto_grupos = texto_grupos + "<a href='/entity-group/"+str(g.grupo.id)+"' style='text-decoration:none; color:#6F8FAF;'>"+g.grupo.groupname+"</a>,&nbsp;"

		return " | " +texto_grupos[:-7]




class BookEntityGroup(models.Model):
	groupname = models.CharField(max_length=512)
	groupinfo = models.TextField()

	def __str__(self):
		return self.groupname

class BookGroupEntity(models.Model):
	entity = models.ForeignKey(BookEntity,on_delete=models.CASCADE)
	grupo = models.ForeignKey(BookEntityGroup,on_delete=models.CASCADE)

	def __str__(self):
		return self.entity.nombre + ' @ ' + self.grupo.groupname


















































