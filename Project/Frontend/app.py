import psycopg2
from flask import Flask, request, redirect, url_for, session
from flask.templating import render_template


app = Flask(__name__,template_folder='template')
app.secret_key = '1524'
app.debug = True

con=psycopg2.connect(host="localhost",database="group_42",user="postgres",password="1524")
cursor_obj=con.cursor()

# function to render index page
@app.route('/')
def home():
    return render_template('home.html')

#function to render create account page
@app.route('/create',methods=["POST"])
def create():
    return redirect('/createred')
@app.route('/createred')
def createred():
    return render_template('create.html')

#function for checking user credentials
@app.route('/checkcred',methods=["POST"])
def checkcred():
    a = "'"+request.form.get("User ID")+"'"
    global uid 
    uid=a
    b = request.form.get("Password")
    sql = '''select * from users where user_id='''+a
    cursor_obj.execute(sql)
    res = cursor_obj.fetchall()
    if(len(res)==0):
        return redirect('/uine')
    if(res[0][4]!=b):
        return redirect('/wrpass')
    if(res[0][5]=="user"):
        return redirect('/user')
    return redirect('/admin')
@app.route('/uine')
def uine():
    return render_template('uine.html')
@app.route('/wrpass')
def wrpass():
    return render_template('wrpass.html')
@app.route('/user')
def user():
    return render_template('user.html')
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/home')
def homerel():
    userid = uid
    sql = '''select * from users where user_id='''+userid
    cursor_obj.execute(sql)
    res = cursor_obj.fetchall()
    if(res[0][5]=="user"):
        return redirect('/user')
    return redirect('/admin')
#function for checking multiple user id and adding account
@app.route('/createac',methods=["POST"])
def createac():
    a = "'"+request.form.get("User ID")+"'"
    b = "'"+request.form.get("Username")+"'"
    c = "'"+request.form.get("Gender")+"'"
    d = "'"+request.form.get("Email")+"'"
    e = "'"+request.form.get("Password")+"'"
    f = "'"+request.form.get("Usertype")+"'"
    g = request.form.get("secretkey")
    sql = '''select * from users where user_id='''+a
    cursor_obj.execute(sql)
    res = cursor_obj.fetchall()
    if(len(res)>0):
        return redirect('/exists')
    if(g!="AKA" and f=="'admin'"):
        return redirect('/wrkey')
    if(a=="''" or b=="''" or c=="''" or d=="''" or e=="''" or f=="''"):
        return redirect('/createred')
    sql1 = '''Insert into users(user_id,user_name,gender,email,password,user_type) Values('''+a+''','''+b+''','''+c+''','''+d+''','''+e+''','''+f+''')'''
    cursor_obj.execute(sql1)
    con.commit()
    return redirect('/created')
@app.route('/exists')
def exists():
    return render_template('userexists.html')
@app.route('/wrkey')
def wrkey():
    return render_template('wrongkey.html')
@app.route('/created')
def created():
    return render_template('accreated.html') 

@app.route('/myprofile')
def myprofile():
    userid=uid
    sql='''select * from users where user_id='''+userid
    cursor_obj.execute(sql)
    profiles = cursor_obj.fetchall()
    return render_template('myprofile.html',profiles=profiles)
@app.route('/deleteuser')
def erase():
    userid=uid
    sql0='''select * from playlist where user_id='''+userid
    cursor_obj.execute(sql0)
    plists=cursor_obj.fetchall()
    for i in plists:
        sql1='''delete from hassong where playlist_id='''+str(i[0])
        sql2='''delete from playlist where playlist_id='''+str(i[0])
        cursor_obj.execute(sql1)
        cursor_obj.execute(sql2)
    sql3='''delete from favourite where user_id='''+userid
    cursor_obj.execute(sql3)
    sql4='''select * from follows where user_id='''+userid
    cursor_obj.execute(sql4)
    artfols=cursor_obj.fetchall()
    if(len(artfols)>0):
        for i in artfols:
            sql5='''Update artist set artist_no_followers=artist_no_followers-1 where artist_id='''+"'"+i[2]+"'"
            cursor_obj.execute(sql5)
    sql6='''delete from follows where user_id='''+userid
    cursor_obj.execute(sql6)
    sql='''delete from users where user_id='''+userid
    cursor_obj.execute(sql)
    con.commit()
    return redirect('/')

@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/mylib')
def mylib():
    userid = uid
    sql = '''select * from playlist where user_id='''+userid+'''order by playlist_id'''
    cursor_obj.execute(sql)
    playlists=cursor_obj.fetchall()
    for i in range(len(playlists)):
        playlist = playlists[i]
        sqla = '''select * from hassong where playlist_id='''+str(playlist[0])+'''limit 1'''
        cursor_obj.execute(sqla)
        song=cursor_obj.fetchall()
        if(len(song)>=1):
            song=song[0][1]
            song="'"+song+"'"
            sqlb = '''select song_id,album_id from songs where song_id='''+song
            cursor_obj.execute(sqlb)
            song=cursor_obj.fetchall()
            song=song[0][1]
            song="'"+song+"'"
            sqlc = '''select album_id,album_image from album where album_id='''+song
            cursor_obj.execute(sqlc)
            song=cursor_obj.fetchall()
            if(len(song)>=1):
                song=song[0][1]
                playlists[i]=playlists[i]+(song,)
            else:
                playlists[i]=playlists[i]+('https://winfort.net/wp-content/themes/consultix-1/images/no-image-found-360x260.png',)
        else:
            playlists[i]=playlists[i]+('https://winfort.net/wp-content/themes/consultix-1/images/no-image-found-360x260.png',)
    return render_template('mylib.html',profiles=playlists)
@app.route('/myart')
def myart():
    userid=uid
    sql='''select artist.artist_id,artist.artist_name,artisi_no_songs,artist_no_followers from artist join follows on artist.artist_id=follows.artist_id where follows.user_id='''+userid
    cursor_obj.execute(sql)
    artists=cursor_obj.fetchall()
    return render_template('myart.html',artists=artists)
@app.route('/fav')
def fav():
    userid=uid
    sql='''select song_id,song_name from favourite where user_id='''+userid+'''order by song_name asc'''
    cursor_obj.execute(sql)
    songs=cursor_obj.fetchall()
    profiles=[]
    for i in songs:
        sql1='''select song_name,song_id,album.album_image,song_duration,song_preview_url from songs  join album on songs.album_id=album.album_id where song_id='''+"'"+i[0]+"'"
        cursor_obj.execute(sql1)
        song=cursor_obj.fetchall()
        for s in song:
            profiles.append(s)
    for i in range(len(profiles)):
        song=profiles[i]
        sqla = '''select * from composedby where composedby.song_id='''+"'"+song[1]+"'"+'''limit 4'''
        cursor_obj.execute(sqla)
        artists=cursor_obj.fetchall()
        artist=()
        for j in artists:
            artist=artist+((j[3],j[2]),)
        profiles[i]=profiles[i]+(artist,)
    return render_template('fav.html',profiles=profiles)
@app.route('/addtofav/<string:a>/<string:b>')
def addtofav(a,b):
    userid=uid
    a="'"+a+"'"
    b="'"+b+"'"
    sql1='''select user_id,user_name from users where user_id='''+userid
    cursor_obj.execute(sql1)
    user=cursor_obj.fetchall()
    sql2= '''Insert into favourite(user_id,user_name,song_id,song_name) Values('''+userid+''','''+"'"+user[0][1]+"'"+''','''+a+''','''+b+''')'''
    cursor_obj.execute(sql2)
    con.commit()
    return ""

@app.route('/removefromfav/<string:a>/<string:b>')
def removefromfav(a,b):
    userid=uid
    a="'"+a+"'"
    b="'"+b+"'"
    sql='''delete from favourite where user_id='''+userid+'''and song_id='''+a
    cursor_obj.execute(sql)
    con.commit()
    return ""

@app.route('/showsongs/<string:a>')
def showsongs(a):
    a="'"+a+"'"
    sql = '''select song_name,song_id,album.album_image,song_duration,song_preview_url from songs join album on songs.album_id=album.album_id where song_language='''+a+'''order by song_popularity desc limit 100'''
    cursor_obj.execute(sql)
    profiles=cursor_obj.fetchall()
    userid=uid
    sqlb = '''select * from favourite where user_id='''+userid
    cursor_obj.execute(sqlb)
    favs=cursor_obj.fetchall()
    favs=[k[2] for k in favs]
    for i in range(len(profiles)):
        song=profiles[i]
        sqla = '''select * from composedby where composedby.song_id='''+"'"+song[1]+"'"+'''limit 4'''
        cursor_obj.execute(sqla)
        artists=cursor_obj.fetchall()
        artist=()
        artistid=()
        for j in artists:
            artist=artist+((j[3],j[2]),)
        profiles[i]=profiles[i]+(artist,)
        if(profiles[i][1] in favs):
            profiles[i]+=(1,)
        else:
            profiles[i]+=(0,)
    userid = uid
    sql = '''select * from playlist where user_id='''+userid+'''order by playlist_id'''
    cursor_obj.execute(sql)
    playlists=cursor_obj.fetchall()
    for i in range(len(playlists)):
        playlist = playlists[i]
        sqla = '''select * from hassong where playlist_id='''+str(playlist[0])+'''limit 1'''
        cursor_obj.execute(sqla)
        song=cursor_obj.fetchall()
        if(len(song)>=1):
            song=song[0][1]
            song="'"+song+"'"
            sqlb = '''select song_id,album_id from songs where song_id='''+song
            cursor_obj.execute(sqlb)
            song=cursor_obj.fetchall()
            song=song[0][1]
            song="'"+song+"'"
            sqlc = '''select album_id,album_image from album where album_id='''+song
            cursor_obj.execute(sqlc)
            song=cursor_obj.fetchall()
            if(len(song)>=1):
                song=song[0][1]
                playlists[i]=playlists[i]+(song,)
            else:
                playlists[i]=playlists[i]+('https://winfort.net/wp-content/themes/consultix-1/images/no-image-found-360x260.png',)
        else:
            playlists[i]=playlists[i]+('https://winfort.net/wp-content/themes/consultix-1/images/no-image-found-360x260.png',)
    return render_template('songs.html',profiles=profiles,playlists=playlists)
@app.route('/createplaylist',methods=["POST"])
def createplaylist():
    userid=uid
    a = "'"+request.form.get("crp")+"'"
    sql = '''select max(playlist_id) from playlist'''
    cursor_obj.execute(sql)
    id=cursor_obj.fetchall()
    id=id[0][0]+1
    sql2= '''Insert into playlist(playlist_id,num_songs,playlist_name,user_id) Values('''+str(id)+''','''+"'"+str(0)+"'"+''','''+a+''','''+userid+''')'''
    cursor_obj.execute(sql2)
    con.commit()
    return redirect('/mylib')
@app.route('/addtoplaylist/<int:a>/<string:b>')
def addtoplaylist(a,b):
    sql0='''select * from hassong where playlist_id='''+str(a)+'''and song_id='''+"'"+b+"'"
    cursor_obj.execute(sql0)
    song=cursor_obj.fetchall()
    if(len(song)==0):
        sql='''Update playlist set num_songs=num_songs+1 where playlist_id='''+str(a)
        sql1='''Insert into hassong(playlist_id,song_id) Values('''+str(a)+''','''+"'"+b+"'"+''')'''
        cursor_obj.execute(sql)
        cursor_obj.execute(sql1)
        con.commit()
    return ""
@app.route('/showplsongs/<int:a>')
def showplsongs(a):
    sql0='''select * from hassong where playlist_id='''+str(a)
    cursor_obj.execute(sql0)
    psongs=cursor_obj.fetchall()
    psongs=[i[1] for i in psongs]
    profiles=[]
    for i in psongs:
        sql1='''select song_name,song_id,album.album_image,song_duration,song_preview_url from songs join album on songs.album_id=album.album_id where song_id='''+"'"+i+"'"
        cursor_obj.execute(sql1)
        song=cursor_obj.fetchall()
        song=song[0]
        profiles.append(song)
    for i in range(len(profiles)):
        song=profiles[i]
        sqla = '''select * from composedby where composedby.song_id='''+"'"+song[1]+"'"+'''limit 4'''
        cursor_obj.execute(sqla)
        artists=cursor_obj.fetchall()
        artist=()
        for j in artists:
            artist=artist+((j[3],j[2]),)
        profiles[i]=profiles[i]+(artist,)
        pid=(a,)
        profiles[i]+=pid
    return render_template('showplsongs.html',profiles=profiles)
@app.route('/removefromplaylist/<int:a>/<string:b>')
def remvoefromplaylist(a,b):
    sql='''Update playlist set num_songs=num_songs-1 where playlist_id='''+str(a)
    sql1='''delete from hassong where playlist_id='''+str(a)+'''and song_id='''+"'"+b+"'"
    cursor_obj.execute(sql)
    cursor_obj.execute(sql1)
    con.commit()
    return ""
@app.route('/deleteplaylist/<int:a>')
def deleteplaylist(a):
    sql='''delete from playlist where playlist_id='''+str(a)
    sql1='''delete from hassong where playlist_id='''+str(a)
    cursor_obj.execute(sql1)
    cursor_obj.execute(sql)
    con.commit()
    return ""
@app.route('/artistsongs/<string:a>')
def artsongs(a):
    a="'"+a+"'"
    userid=uid
    global currart
    currart=a
    sql00='''select * from follows where user_id='''+userid+'''and artist_id='''+a
    cursor_obj.execute(sql00)
    isfol=cursor_obj.fetchall()
    count=0
    if(len(isfol)>0):
        count=1
    sql0='''select * from composedby where artist_id='''+a
    cursor_obj.execute(sql0)
    artsongs=cursor_obj.fetchall()
    artsongs=[i[0] for i in artsongs]
    profiles=[]
    for i in artsongs:
        sql1='''select song_name,song_id,album.album_image,song_duration,song_preview_url from songs join album on songs.album_id=album.album_id where song_id='''+"'"+i+"'"
        cursor_obj.execute(sql1)
        song=cursor_obj.fetchall()
        song=song[0]
        profiles.append(song)
    userid=uid
    sqlb = '''select * from favourite where user_id='''+userid
    cursor_obj.execute(sqlb)
    favs=cursor_obj.fetchall()
    favs=[k[2] for k in favs]
    for i in range(len(profiles)):
        song=profiles[i]
        sqla = '''select * from composedby where composedby.song_id='''+"'"+song[1]+"'"+'''limit 4'''
        cursor_obj.execute(sqla)
        artists=cursor_obj.fetchall()
        artist=()
        artistid=()
        for j in artists:
            artist=artist+((j[3],j[2]),)
        profiles[i]=profiles[i]+(artist,)
        if(profiles[i][1] in favs):
            profiles[i]+=(1,)
        else:
            profiles[i]+=(0,)
    userid = uid
    sql = '''select * from playlist where user_id='''+userid+'''order by playlist_id'''
    cursor_obj.execute(sql)
    playlists=cursor_obj.fetchall()
    for i in range(len(playlists)):
        playlist = playlists[i]
        sqla = '''select * from hassong where playlist_id='''+str(playlist[0])+'''limit 1'''
        cursor_obj.execute(sqla)
        song=cursor_obj.fetchall()
        if(len(song)>=1):
            song=song[0][1]
            song="'"+song+"'"
            sqlb = '''select song_id,album_id from songs where song_id='''+song
            cursor_obj.execute(sqlb)
            song=cursor_obj.fetchall()
            song=song[0][1]
            song="'"+song+"'"
            sqlc = '''select album_id,album_image from album where album_id='''+song
            cursor_obj.execute(sqlc)
            song=cursor_obj.fetchall()
            if(len(song)>=1):
                song=song[0][1]
                playlists[i]=playlists[i]+(song,)
            else:
                playlists[i]=playlists[i]+('https://winfort.net/wp-content/themes/consultix-1/images/no-image-found-360x260.png',)
        else:
            playlists[i]=playlists[i]+('https://winfort.net/wp-content/themes/consultix-1/images/no-image-found-360x260.png',)
    return render_template('artsongs.html',profiles=profiles,playlists=playlists,count=count)
@app.route('/albumsongs/<string:a>')
def albumsongs(a):
    a="'"+a+"'"
    sql0='''select * from songs where album_id='''+a
    cursor_obj.execute(sql0)
    albsongs=cursor_obj.fetchall()
    albsongs=[i[0] for i in albsongs]
    profiles=[]
    for i in albsongs:
        sql1='''select song_name,song_id,album.album_image,song_duration,song_preview_url from songs join album on songs.album_id=album.album_id where song_id='''+"'"+i+"'"
        cursor_obj.execute(sql1)
        song=cursor_obj.fetchall()
        song=song[0]
        profiles.append(song)
    userid=uid
    sqlb = '''select * from favourite where user_id='''+userid
    cursor_obj.execute(sqlb)
    favs=cursor_obj.fetchall()
    favs=[k[2] for k in favs]
    for i in range(len(profiles)):
        song=profiles[i]
        sqla = '''select * from composedby where composedby.song_id='''+"'"+song[1]+"'"+'''limit 4'''
        cursor_obj.execute(sqla)
        artists=cursor_obj.fetchall()
        artist=()
        artistid=()
        for j in artists:
            artist=artist+((j[3],j[2]),)
        profiles[i]=profiles[i]+(artist,)
        if(profiles[i][1] in favs):
            profiles[i]+=(1,)
        else:
            profiles[i]+=(0,)
    userid = uid
    sql = '''select * from playlist where user_id='''+userid+'''order by playlist_id'''
    cursor_obj.execute(sql)
    playlists=cursor_obj.fetchall()
    for i in range(len(playlists)):
        playlist = playlists[i]
        sqla = '''select * from hassong where playlist_id='''+str(playlist[0])+'''limit 1'''
        cursor_obj.execute(sqla)
        song=cursor_obj.fetchall()
        if(len(song)>=1):
            song=song[0][1]
            song="'"+song+"'"
            sqlb = '''select song_id,album_id from songs where song_id='''+song
            cursor_obj.execute(sqlb)
            song=cursor_obj.fetchall()
            song=song[0][1]
            song="'"+song+"'"
            sqlc = '''select album_id,album_image from album where album_id='''+song
            cursor_obj.execute(sqlc)
            song=cursor_obj.fetchall()
            if(len(song)>=1):
                song=song[0][1]
                playlists[i]=playlists[i]+(song,)
            else:
                playlists[i]=playlists[i]+('https://winfort.net/wp-content/themes/consultix-1/images/no-image-found-360x260.png',)
        else:
            playlists[i]=playlists[i]+('https://winfort.net/wp-content/themes/consultix-1/images/no-image-found-360x260.png',)
    return render_template('songs.html',profiles=profiles,playlists=playlists)
@app.route('/allartists')
def allartists():
    sql='''select * from artist order by artist_no_followers desc'''
    cursor_obj.execute(sql)
    artists=cursor_obj.fetchall()
    return render_template('allartists.html',artists=artists)
@app.route('/allalbums')
def allalbums():
    sql='''select * from album limit 500'''
    cursor_obj.execute(sql)
    albums=cursor_obj.fetchall()
    return render_template('allalbums.html',albums=albums)
@app.route('/unfollow/<string:a>')
def unfollow(a):
    userid=uid
    sql='''Update artist set artist_no_followers=artist_no_followers-1 where artist_id='''+"'"+a+"'"
    sql1='''delete from follows where artist_id='''+"'"+a+"'"+'''and user_id='''+userid
    cursor_obj.execute(sql)
    cursor_obj.execute(sql1)
    con.commit()
    return ""
@app.route('/unfollowart')
def unfollow1():
    userid=uid
    a=currart
    sql='''Update artist set artist_no_followers=artist_no_followers-1 where artist_id='''+a
    sql1='''delete from follows where artist_id='''+a+'''and user_id='''+userid
    cursor_obj.execute(sql)
    cursor_obj.execute(sql1)
    con.commit()
    return ""
@app.route('/follow')
def follow():
    userid=uid
    a=currart
    sql1='''select user_id,user_name from users where user_id='''+userid
    cursor_obj.execute(sql1)
    user=cursor_obj.fetchall()
    username="'"+user[0][1]+"'"
    sql1='''select artist_id,artist_name from artist where artist_id='''+a
    cursor_obj.execute(sql1)
    art=cursor_obj.fetchall()
    artname="'"+art[0][1]+"'"
    sql='''Update artist set artist_no_followers=artist_no_followers+1 where artist_id='''+a
    sql1='''Insert into follows(user_id,user_name,artist_id,artist_name) Values('''+userid+''','''+username+''','''+a+''','''+artname+''')'''
    cursor_obj.execute(sql)
    cursor_obj.execute(sql1)
    con.commit()
    return ""
@app.route('/searchartist',methods=["POST"])
def searchart():
    a = "'%"+request.form.get("ArtName")+"%'"
    sql='''select * from artist where artist_name like'''+a+'''order by artist_no_followers desc'''
    cursor_obj.execute(sql)
    artists=cursor_obj.fetchall()
    session['artists'] = artists
    return redirect(url_for('searchar'))
@app.route('/searchar')
def searchar():
    artists = session.get('artists')
    return render_template('allartists.html',artists=artists)

@app.route('/searchalbum',methods=["POST"])
def searchalbum():
    a = "'%"+request.form.get("AlbumName")+"%'"
    sql='''select * from album where album_name like'''+a+'''order by album_name desc limit 500'''
    cursor_obj.execute(sql)
    albums=cursor_obj.fetchall()
    session['albums'] = albums
    return redirect(url_for('searchalbu'))
@app.route('/searchalbu')
def searchalbu():
    albums = session.get('albums')
    return render_template('allalbums.html',albums=albums)

@app.route('/searchsong',methods=["POST"])
def searchsong():
    a = "'%"+request.form.get("SongName")+"%'"
    sql='''select song_id,song_name from songs where song_name like'''+a+''' limit 200'''
    cursor_obj.execute(sql)
    songs=cursor_obj.fetchall()
    songs=[i[0] for i in songs]
    session['songs'] = songs
    return redirect(url_for('searchson'))
@app.route('/searchson')
def searchson():
    albsongs = session.get('songs')
    profiles=[]
    for i in albsongs:
        sql1='''select song_name,song_id,album.album_image,song_duration,song_preview_url from songs join album on songs.album_id=album.album_id where song_id='''+"'"+i+"'"
        cursor_obj.execute(sql1)
        song=cursor_obj.fetchall()
        song=song[0]
        profiles.append(song)
    userid=uid
    sqlb = '''select * from favourite where user_id='''+userid
    cursor_obj.execute(sqlb)
    favs=cursor_obj.fetchall()
    favs=[k[2] for k in favs]
    for i in range(len(profiles)):
        song=profiles[i]
        sqla = '''select * from composedby where composedby.song_id='''+"'"+song[1]+"'"+'''limit 4'''
        cursor_obj.execute(sqla)
        artists=cursor_obj.fetchall()
        artist=()
        artistid=()
        for j in artists:
            artist=artist+((j[3],j[2]),)
        profiles[i]=profiles[i]+(artist,)
        if(profiles[i][1] in favs):
            profiles[i]+=(1,)
        else:
            profiles[i]+=(0,)
    userid = uid
    sql = '''select * from playlist where user_id='''+userid+'''order by playlist_id'''
    cursor_obj.execute(sql)
    playlists=cursor_obj.fetchall()
    for i in range(len(playlists)):
        playlist = playlists[i]
        sqla = '''select * from hassong where playlist_id='''+str(playlist[0])+'''limit 1'''
        cursor_obj.execute(sqla)
        song=cursor_obj.fetchall()
        if(len(song)>=1):
            song=song[0][1]
            song="'"+song+"'"
            sqlb = '''select song_id,album_id from songs where song_id='''+song
            cursor_obj.execute(sqlb)
            song=cursor_obj.fetchall()
            song=song[0][1]
            song="'"+song+"'"
            sqlc = '''select album_id,album_image from album where album_id='''+song
            cursor_obj.execute(sqlc)
            song=cursor_obj.fetchall()
            if(len(song)>=1):
                song=song[0][1]
                playlists[i]=playlists[i]+(song,)
            else:
                playlists[i]=playlists[i]+('https://winfort.net/wp-content/themes/consultix-1/images/no-image-found-360x260.png',)
        else:
            playlists[i]=playlists[i]+('https://winfort.net/wp-content/themes/consultix-1/images/no-image-found-360x260.png',)
    return render_template('songs.html',profiles=profiles,playlists=playlists)
if __name__ == '__main__':
	app.run()

