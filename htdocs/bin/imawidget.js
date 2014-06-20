/**
 * @file script.js - Drag and resize example for Dean. <br>
 * Created: 02/17/2013<br>
 * Modified: 02/17/2014
 * @version 1.0.0
*/

/**
 * DEAN
 * @namespace
 * @type {object}
 * @global
 * @public
*/
var DEAN = window.DEAN || {},
    offset_data; //Global variable as Chrome doesn't allow access to event.dataTransfer in dragover.


/**
 * Immediately-Invoked Function Expression.
 *
 * @function
 * @param {object} w - Global window object.
 * @param {object} d - Global document object.
*/
(function (w, d) {

    // This is strict mode js. There is no safety net!
    'use strict';

    /**
     * Creates an instance of FocusConstructor.<br>
     * Modified: 02/17/2013
     *
     * @constructor
     * @param {string} target - Class name of ad container element.
     * @author Richard Dillman <rdillman@gmail.com>
    */
    DEAN.FocusConstructor = function () {};

    /**
     * Inheritable methods.
     *
     * @type {object}
    */
    DEAN.FocusConstructor.prototype = {

        /**
         * Initialization methods.<br>
         * Modified: 02/17/2013
         *
         * @method init
         * @param {object} data - The body attributes data array.
         * @author Richard Dillman <rdillman@gmail.com>
         * @public
        */
        init: function () {

            // Get all the elements we will be using.
            this.form       = d.getElementById('imageSizer');
            this.imgSrc     = d.getElementById('imgSrc');
            this.imgDisplay = d.getElementById('imgDisplay');
            this.box        = d.getElementById('box');
            this.top        = d.getElementById('top');
            this.right      = d.getElementById('right');
            this.bottom     = d.getElementById('bottom');
            this.left       = d.getElementById('left');
            this.send       = d.getElementById('send');
            this.attach();

        },

        /**
         * All functions attached to dom elements.<br>
         * Modified: 02/17/2013
         *
         * @method attach
         * @author Richard Dillman <rdillman@gmail.com>
         * @public
        */
        attach: function () {

            // Varialbes
            var p = DEAN.Focus;

            p.box.addEventListener('dragstart', DEAN.Focus.drag_start, false);
            d.body.addEventListener('dragover', DEAN.Focus.drag_over, false);
            d.body.addEventListener('drop', DEAN.Focus.drop, false);

            // When the image source changed update the image and reset the box.
            p.imgSrc.onchange = function (e) {

                e.preventDefault();

                // We only want to update the image if we hve a valid url.
                if (p.validate()) {
                    p.updateImage(p.imgDisplay, p.imgSrc.value);
                }
            };

            // If we have valid data submit the form.
            p.send.onclick = function (e) {

                e.preventDefault();

                if (p.validate()) {
                    p.sendData();
                }
            };

        },

        /**
         * Validate the form.<br>
         * Modified: 02/17/2013
         *
         * @method validate
         * @author Richard Dillman <rdillman@gmail.com>
         * @public
        */
        validate: function () {
            return this.imgSrc.value.match(/(^|\s)((https?:\/\/)?[\w-]+(\.[\w-]+)+\.?(:\d+)?(\/\S*)?)/gi) ? true : false;
        },

        /**
         * Update the images source, and reset the position of the box.<br>
         * Modified: 02/17/2013
         *
         * @method updateImage
         * @author Richard Dillman <rdillman@gmail.com>
         * @param {object} target - The element to alter.
         * @param {string} source - The url for the new image source.
         * @public
        */
        updateImage: function (target, source) {
            target.src = source;
            DEAN.Focus.box.style.left = '10px';
            DEAN.Focus.box.style.top = '10px';
        },

        /**
         * Events to fire when begining the drag.
         * Modified: 02/17/2013
         *
         * @method drag_start
         * @author Richard Dillman <rdillman@gmail.com>
         * @public
        */
        drag_start: function (event) {

            // Variables
            var style = window.getComputedStyle(event.target, null);

            offset_data = (parseInt(style.getPropertyValue("left"), 10) - event.clientX) + ',' + (parseInt(style.getPropertyValue("top"), 10) - event.clientY);
            event.dataTransfer.setData("text/plain", offset_data);

        },

        /**
         * Events to fire when dragging over the target.
         * Modified: 02/17/2013
         *
         * @method drag_over
         * @author Richard Dillman <rdillman@gmail.com>
         * @public
        */
        drag_over: function (event) {

            // Variables
            var offset;

            try {
                offset = event.dataTransfer.getData("text/plain").split(',');
            } catch (e) {
                offset = offset_data.split(',');
            }

            DEAN.Focus.box.style.left = (event.clientX + parseInt(offset[0], 10)) + 'px';
            DEAN.Focus.box.style.top = (event.clientY + parseInt(offset[1], 10)) + 'px';
            event.preventDefault();

            return false;

        },

        /**
         * Events to fire when dropping.
         * Modified: 02/17/2013
         *
         * @method drop
         * @author Richard Dillman <rdillman@gmail.com>
         * @public
        */
        drop: function (event) {

            // Variables
            var offset;

            try {
                offset = event.dataTransfer.getData("text/plain").split(',');
            } catch (e) {
                offset = offset_data.split(',');
            }

            DEAN.Focus.box.style.left = (event.clientX + parseInt(offset[0], 10)) + 'px';
            DEAN.Focus.box.style.top = (event.clientY + parseInt(offset[1], 10)) + 'px';
            event.preventDefault();

            return false;

        },

        /**
         * Send the form data.
         * Modified: 02/17/2013
         *
         * @method sendData
         * @author Richard Dillman <rdillman@gmail.com>
         * @public
        */
        sendData: function () {

            var p = DEAN.Focus;

            p.top.value = p.box.offsetTop;
            p.left.value = p.box.offsetLeft;
            p.bottom.value = p.box.offsetTop + p.box.offsetHeight;
            p.right.value = p.box.offsetLeft + p.box.offsetWidth;
            p.form.submit();
        }

    };

}(window, document));

// Create a new instance of DEAN.
DEAN.Focus = new DEAN.FocusConstructor();

// Initialize the new DEAN Focus object.
DEAN.Focus.init();



/*

// ImaWidget - Simple Image Bounding Widget
// Written by Dean Dierschow sometime in 200X.

// This applet is started with a url for an image.  That image is
// displayed, and a bounding rectangle can be specified with the mouse.
// Any side can be grabbed and moved.  The coordinates can be sent back
// to the browser for form submission.

// Known bugs:
//  * Grabbing anywhere on the line that any side is on grabs that
//    side -- even if it's outside the limits of the rectangle.
//  * There is no way to clear the rectagle once it is set.

// Features that would be nice to add:
//  * Single click not on the rectangle should clear the rectangle.
//  * Grabbing a corner should allow you to move two sides at once.
//  * Since the rectangle is black, this thing is damn near unusable
//    with a dark image.  Some way to fix that would be nice.

import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;
import java.applet.*;
import java.applet.Applet;
import java.lang.*;
import java.net.*;
import java.net.URL;
import javax.swing.*;
import javax.swing.event.*;


public class ImaWidget extends JApplet implements MouseListener, MouseMotionListener, Runnable
{

    Image img;
    MediaTracker trk;
    boolean whoa = false;
    Color colorBg = Color.black;

    static final int ERROR_PAGE = -1;
    static final int LOADING = 0;
    static final int EDITING = 1;

    int screen = LOADING;

    // the two points that define the rectangle
    Point pntStart = new Point();
    Point pntEnd = new Point();
    boolean showrect = false;
    boolean editrectx = false;
    boolean editrecty = false;

    int curcur = Cursor.DEFAULT_CURSOR;
    Cursor curdefault = getCursor();
    Cursor curw = new Cursor(Cursor.W_RESIZE_CURSOR);
    Cursor curn = new Cursor(Cursor.N_RESIZE_CURSOR);
    Cursor cure = new Cursor(Cursor.E_RESIZE_CURSOR);
    Cursor curs = new Cursor(Cursor.S_RESIZE_CURSOR);

    // -- JApplet interface

    public void init ()
    {
	super.init();
	System.out.println("imawidget in init.");
	System.out.println(getCodeBase());
	System.out.println(getDocumentBase());
	System.out.println(getParameter("file"));
	trk = new MediaTracker(this);

	Container Panel = getContentPane();
	Panel.setBackground(Color.black);

	addMouseListener(this);
	addMouseMotionListener(this);

	repaint();

	Thread th = new Thread(this);
	th.start();
    }

    public int LoadImage(String name)
    {
	img = getImage(getDocumentBase(), name);

	img.flush();
        trk.addImage(img,0);
        try
	{
            trk.waitForID(0);
        }
	catch (InterruptedException e) { }

        // check for errors
        if (trk.isErrorAny())
	{
            return 2;
	}
        else if (trk.checkAll())
	{
            return 0;
        }
	return 1;
    } // load Images

    public void start()
    {
	System.out.println("imawidget in start.");
    }

    public void stop()
    {
	System.out.println("imawidget in stop.");
	whoa = true;
    }

    public void destroy()
    {
	System.out.println("imawidget in destroy.");
    }

    // override update so it doesn't erase screen
    public void update(Graphics g)
    {
	System.out.println("imawidget in update.");
	paint(g);
    } // update

    public void paint(Graphics g)
    {
	//super.paint(g);
		System.out.println("imawidget in paint."+screen);
        switch (screen)
	{
        case EDITING:
	    g.drawImage(img, 0, 0, this);
	    if (showrect)
	    {
		int [] carr = coords();
		g.drawRect(carr[0], carr[1], carr[2] - carr[0], carr[3] - carr[1]);
	    }
	    break;
	}

    } // paint

    // ----- Runnable interface

    public void run()
    {
	System.out.println("imawidget in run.");
	int tickValue = -1;
        while (! whoa)
	{
	    if (screen == LOADING)
	    {
		int err = LoadImage(getParameter("file"));
		if (err > 0)
		{
		    screen = ERROR_PAGE;
		    System.out.println("screen"+screen);
		}
		else
		{
		    screen++;
		    System.out.println("screen"+screen);
		}
		resize(img.getWidth(this), img.getHeight(this));
		repaint();
	    }
	    else if (screen != ERROR_PAGE)
		tickValue = tick();

            try
	    {
		if (tickValue >= 0)
		{
		    System.out.println("imawidget tick sleep.");
		    Thread.currentThread().sleep(tickValue);
		}
		else
		{
		    //System.out.println("imawidget tick yield.");
		    Thread.currentThread().yield();
		}
            }
	    catch (Exception exc) { };
        }
	Thread.currentThread().interrupt();
	System.out.println("imawidget run whoa.");
    }  // run

    // ----- MouseListener interface

    public void mouseDragged(MouseEvent evt)
    {
	if (drag(evt.getPoint()))
	{
	    repaint();
	}
    }
    public void mouseMoved(MouseEvent evt)
    {
	Point pnt = evt.getPoint();
	if (move(pnt))
	{
	    //repaint();
	}
	cursorSet(pnt);
    }

    public void cursorSet(Point pnt)
    {
	if (abs(pnt.x - pntStart.x) < 2)
	{
	    if (curcur != Cursor.W_RESIZE_CURSOR)
	    {
		setCursor(curw);
		curcur = Cursor.W_RESIZE_CURSOR;
	    }
	}
	else if (abs(pnt.y - pntStart.y) < 2)
	{
	    if (curcur != Cursor.N_RESIZE_CURSOR)
	    {
		setCursor(curn);
		curcur = Cursor.N_RESIZE_CURSOR;
	    }
	}
	else if (abs(pnt.x - pntEnd.x) < 2)
	{
	    if (curcur != Cursor.E_RESIZE_CURSOR)
	    {
		setCursor(cure);
		curcur = Cursor.E_RESIZE_CURSOR;
	    }
	}
	else if (abs(pnt.y - pntEnd.y) < 2)
	{
	    if (curcur != Cursor.S_RESIZE_CURSOR)
	    {
		setCursor(curs);
		curcur = Cursor.S_RESIZE_CURSOR;
	    }
	}
	else
	{
	    if (curcur != Cursor.DEFAULT_CURSOR)
	    {
		setCursor(curdefault);
		curcur = Cursor.DEFAULT_CURSOR;
	    }
	}
    }
    public void mouseEntered(MouseEvent evt) { }
    public void mouseExited(MouseEvent evt) { }
    public void mousePressed(MouseEvent evt)
    {
	//setCursor(curdefault);
	curcur = Cursor.DEFAULT_CURSOR;
	if (press(evt.getPoint()))
	{
	    repaint();
	}
    }
    public void mouseReleased(MouseEvent evt)
    {
	setCursor(curdefault);
	curcur = Cursor.DEFAULT_CURSOR;
	if (release(evt.getPoint()))
	{
	    repaint();
	}
    }
    public void mouseClicked(MouseEvent evt)
    {
	if (click(evt.getPoint(), evt.getClickCount()))
	{
	    repaint();
	}
    }

    // -- Higher level mouse thingies

    public boolean drag(Point pnt)
    {
	pnt.x = Math.max(Math.min(pnt.x, img.getWidth(this)), 0);
	pnt.y = Math.max(Math.min(pnt.y, img.getHeight(this)), 0);
	System.out.println("imawidget in drag: "+pnt+"/"+editrectx+"/"+editrecty);
	if (editrectx)
	{
	    pntStart.x = pnt.x;
	}
	else if (editrecty)
	{
	    pntStart.y = pnt.y;
	}
	else
	{
	    pntEnd.setLocation(pnt);
	}
	System.out.println("" + pntStart + pntEnd);
	cursorSet(pnt);
	return true;
    }

    public boolean press(Point pnt)
    {
	System.out.println("imawidget in press."+pnt);
	if (showrect)
	{
	    if (abs(pnt.x - pntStart.x) < 2)
	    {
		editrectx = true;
		System.out.println("editing x" + pntStart + ", " + pntEnd);
	    }
	    else if (abs(pnt.y - pntStart.y) < 2)
	    {
		editrecty = true;
		System.out.println("editing y" + pntStart + ", " + pntEnd);
	    }
	    else if (abs(pnt.x - pntEnd.x) < 2)
	    {
		editrectx = true;
		Point hold = pntEnd;
		pntEnd = pntStart;
		pntStart = hold;
		System.out.println("editing x" + pntStart + ", " + pntEnd);
	    }
	    else if (abs(pnt.y - pntEnd.y) < 2)
	    {
		editrecty = true;
		Point hold = pntEnd;
		pntEnd = pntStart;
		pntStart = hold;
		System.out.println("editing y" + pntStart + ", " + pntEnd);
	    }
	    else
	    {
		editrectx = editrecty = false;
		pntStart.setLocation(pnt);
		pntEnd.setLocation(pnt);
		System.out.println("restarting");
	    }
	}
	else
	{
	    editrectx = editrecty = false;
	    pntStart.setLocation(pnt);
	    pntEnd.setLocation(pnt);
	    System.out.println("starting");
	}
	showrect = true;

	return true;
    }

    public boolean release(Point pnt)
    {
	System.out.println("imawidget in release."+pnt);
	editrectx = editrecty = false;
	return true;
    }

    public boolean click(Point pnt, int count)
    {
	System.out.println("imawidget in click."+pnt);
	switch (screen)
	{
	case LOADING:
	    break;
	case EDITING:
	    break;
	}
	return true;
    }

    public boolean move(Point pnt) { return false; }

    public int tick()
    {
	switch (screen)
	{
	case EDITING:
	    return -1;
	default:
	    break;
	}
	return -1;
    }  // tick

    // -- invoked by the web page to extract information

    public String getCoords()
    {
	int [] carr = coords();
	//String s = ""+x1+","+y1+","+x2+","+y2;
	String s = ""+carr[0]+","+carr[1]+","+carr[2]+","+carr[3];
	System.out.println("imawidget in getCoords." + s);
	return s;
    }

    public int [] coords()
    {
	if (!showrect)
	{
	    int [] carr = {0, 0, img.getWidth(this), img.getHeight(this)};
	    return carr;
	}
	int x1 = pntStart.x;
	int y1 = pntStart.y;
	int x2 = pntEnd.x;
	int y2 = pntEnd.y;
	if (x1 > x2)
	{
	    int x = x2;
	    x2 = x1;
	    x1 = x;
	}
	if (y1 > y2)
	{
	    int y = y2;
	    y2 = y1;
	    y1 = y;
	}
	int [] carr = {x1, y1, x2, y2};
	return carr;
    }

    public int abs(int v)
    {
	if (v < 0)
	    return -v;
	return v;
    }

}
*/
