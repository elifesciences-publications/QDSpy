#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
genlock API for NVidia and AMD graphic cards

Copyright (c) 2013-2016 Thomas Euler
All rights reserved.
"""
# ---------------------------------------------------------------------
__author__ 	= "code@eulerlab.de"

import ctypes
import pyglet
import pyglet.gl.wglext_nv as nv
import pyglet.gl.wglext_arb as amd
  
# ---------------------------------------------------------------------
class GenlockType:
  genlock_none   = 0
  genlock_AMD    = 1  
  genlock_NVIDIA = 2


GenlockTypeStr   = dict([
  (GenlockType.genlock_none,   "none"),
  (GenlockType.genlock_AMD,    "AMD API"),
  (GenlockType.genlock_NVIDIA, "Nvidia API"),
  ])
  
# =====================================================================
#
# ---------------------------------------------------------------------
class Genlock:
  """ Encapsulates the genlock API
  """
  def __init__(self, funcLog=None):
    # Check if genlock is available
    #
    self.type = GenlockType.genlock_none
    if funcLog == None:
      self.log = self.__log
    else:
      self.log = funcLog
    
    self.HDC  = pyglet.gl.get_current_context()._context
    res       = pyglet.gl.wgl_info.have_extension("WGL_I3D_genlock")
    c_flag    = ctypes.c_long()
    if res:
      # Check for Nvidia API
      #
      try:
        nv.wglIsEnabledGenlockI3D(self.HDC, ctypes.pointer(c_flag))
        self.type = GenlockType.genlock_NVIDIA
      except pyglet.gl.lib.MissingFunctionException:
        pass

      # Check for AMD API
      #
      try:
        amd.wglIsEnabledGenlockI3D(self.HDC, ctypes.pointer(c_flag))
        self.type = GenlockType.genlock_AMD
      except pyglet.gl.lib.MissingFunctionException:
        pass
        
    self.log("ok" if self.type != GenlockType.genlock_none else "error", 
             "Genlock: " +GenlockTypeStr[self.type] +" supported")
      
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  def isEnabledGenlock(self):
    """ Returns tuple (result, flag) with
          result := result of API call
          flag   := True if genlock is enabled
    """
    c_flag = ctypes.c_long(0)
    res    = 0
    if self.type == GenlockType.genlock_AMD:
      res = amd.wglIsEnabledGenlockI3D(self.HDC, ctypes.pointer(c_flag))
    elif self.type == GenlockType.genlock_NVIDIA:
      res = nv.wglIsEnabledGenlockI3D(self.HDC, ctypes.pointer(c_flag))
      
    return (res, c_flag.value)  

  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  def __log (self, sHeader, sMsg):
    print("{0!s:>8} {1}".format(sHeader, sMsg))

# ---------------------------------------------------------------------
"""
hdc   = pyglet.gl.get_current_context()
res   = pyglet.gl.wgl_info.have_extension("WGL_I3D_genlock")
print("WGL_I3D_genlock extention", res)

c_res  = ctypes.c_bool()
c_flag = ctypes.c_long()


c_res  = pyglet.gl.wglext_arb.wglIsEnabledGenlockI3D(hdc._context, ctypes.pointer(c_flag))
print("wglIsEnabledGenlockI3D = ", c_res, c_flag.value)

c_res  = pyglet.gl.wglext_arb.wglDisableGenlockI3D(hdc._context)
print("wglDisableGenlockI3D = ", c_res)
"""

"""
Name

    WGL_I3D_genlock

Name Strings

    WGL_I3D_genlock

Contact

    Dale Kirkland, Intense3D (kirkland 'at' intense3d.com)

Status

    Complete

Version

    Date: 04/17/2000   Revision 1.0

Number

    252

Dependencies

    The extension is written against the OpenGL 1.2.1 Specification
    although it should work on any previous OpenGL specification.

    The WGL_EXT_extensions_string extension is required.

Overview

    The genlock extensions allows application control of the genlock
    features.  Genlock is used to synchronize the refresh of the
    monitor to an external signal.

    There are five different parameters that can be used to control
    genlock:

         Enable/Disable
         Source Selection
         Source Sample Edge
         Source Sample Rate
         Source Delay

IP Status

    None

Issues

    None

New Procedures and Functions

    BOOL wglEnableGenlockI3D(HDC hDC)

    BOOL wglDisableGenlockI3D(HDC hDC)

    BOOL wglIsEnabledGenlockI3D(HDC hDC,
                                BOOL *pFlag)

    BOOL wglGenlockSourceI3D(HDC hDC,
                             UINT uSource)

    BOOL wglGetGenlockSourceI3D(HDC hDC,
                                UINT *uSource)

    BOOL wglGenlockSourceEdgeI3D(HDC hDC,
                                 UINT uEdge)

    BOOL wglGetGenlockSourceEdgeI3D(HDC hDC,
                                    UINT *uEdge)

    BOOL wglGenlockSampleRateI3D(HDC hDC,
                                 UINT uRate)

    BOOL wglGetGenlockSampleRateI3D(HDC hDC,
                                    UINT *uRate)

    BOOL wglGenlockSourceDelayI3D(HDC hDC,
                                  UINT uDelay)

    BOOL wglGetGenlockSourceDelayI3D(HDC hDC,
                                      UINT *uDelay)

    BOOL wglQueryGenlockMaxSourceDelayI3D(HDC hDC,
                                          UINT *uMaxLineDelay,
                                          UINT *uMaxPixelDelay)

New Tokens

    Accepted by the <uSource> parameter of wglGenlockSourceI3D:

      WGL_GENLOCK_SOURCE_MULTIVIEW_I3D            0x2044
      WGL_GENLOCK_SOURCE_EXTERNAL_SYNC_I3D        0x2045
      WGL_GENLOCK_SOURCE_EXTERNAL_FIELD_I3D       0x2046
      WGL_GENLOCK_SOURCE_EXTERNAL_TTL_I3D         0x2047
      WGL_GENLOCK_SOURCE_DIGITAL_SYNC_I3D         0x2048
      WGL_GENLOCK_SOURCE_DIGITAL_FIELD_I3D        0x2049

    Accepted by the <uEdge> parameter of wglGenlockSourceEdgeI3D:

      WGL_GENLOCK_SOURCE_EDGE_FALLING_I3D         0x204A
      WGL_GENLOCK_SOURCE_EDGE_RISING_I3D          0x204B
      WGL_GENLOCK_SOURCE_EDGE_BOTH_I3D            0x204C

Additions to Chapter 2 of the OpenGL 1.2.1 Specification (OpenGL Operation)

    None

Additions to Chapter 3 of the OpenGL 1.2.1 Specification (Rasterization)

    None

Additions to Chapter 4 of the OpenGL 1.2.1 Specification (Per-Fragment
Operations and the Frame Buffer)

    None

Additions to Chapter 5 of the OpenGL 1.2.1 Specification (Special Functions)

    None

Additions to Chapter 6 of the OpenGL 1.2.1 Specification (State and
State Requests)

    None

Additions to Appendix A of the OpenGL 1.2.1 Specification (Invariance)

    None

Additions to the WGL Specification

    The genlock trigger is used to synchronize the start of a frame
    with a trigger pulse.  If field data is being displayed (e.g.
    frame-sequential stereo), the synchronization only occurs at the
    frame boundary, not each field boundary.

    The genlock trigger is derived from the genlock source.  The
    genlock source can be selected from six different inputs to the
    system by calling wglGenlockSourceI3D.

      BOOL wglGenlockSourceI3D(HDC hDC,
                               UINT uSource)

    <hDC> is a device context for the graphics adapter or a window
    residing on the graphics adapter that supports genlock.  There is
    only a single genlock source for each graphics adapter regardless
    of the number of monitors supported by the adapter.

    <uSource> specifies one of the following sources:

      WGL_GENLOCK_SOURCE_MULTIVIEW_I3D
        Selects the multiview sync signal as the genlock source.

      WGL_GENLOCK_SOURCE_EXTERNAL_SYNC_I3D
        Selects the external genlock vertical sync component.

      WGL_GENLOCK_SOURCE_EXTERNAL_FIELD_I3D
        Selects the external genlock field component.

      WGL_GENLOCK_SOURCE_EXTERNAL_TTL_I3D
        Selects the external genlock as a TTL-level signal.

      WGL_GENLOCK_SOURCE_DIGITAL_SYNC_I3D
        Selects the digital genlock vertical sync component.

      WGL_GENLOCK_SOURCE_DIGITAL_FIELD_I3D
        Selects the digital genlock field component.

    The current genlock source can be queried by calling
    wglGetGenlockSourceI3D.

    A genlock pulse is generated from the input source based on the
    rising, falling, or both edges of the source.  The edge selection
    is set by calling wglGenlockSourceEdgeI3D.

      BOOL wglGenlockSourceEdgeI3D(HDC hDC,
                                   UINT uEdge)

    <uEdge> specifies one of the following source edges modes used
    to generate the genlock trigger.

      WGL_GENLOCK_SOURCE_EDGE_FALLING_I3D
        Selects the falling edge of the source.

      WGL_GENLOCK_SOURCE_EDGE_RISING_I3D
        Selects the rising edge of the source.

      WGL_GENLOCK_SOURCE_EDGE_BOTH_I3D
        Selects both edges of the source.

    The current genlock source edge mode can be queried with
    wglGetGenlockSourceEdgeI3D.

    The genlock trigger is generated by sampling the genlock pulses.
    The sample rate of the genlock pulses is controlled by calling
    wglGenlockSampleRateI3D.

      BOOL wglGenlockSampleRateI3D(HDC hDC,
                                   UINT uRate)

    <uRate> specifies every nth pulse be used for the genlock trigger.
    For example, if <uRate> were set to a value of 2, every other
    genlock pulse would generate a genlock trigger.  The minimum
    value for <uRate> is 1.  The maximum value for <uRate> is 6.

    The current genlock sample rate can be queried by calling
    wglGetGenlockSampleRateI3D.

    The genlock trigger can be delayed up to an entire frame by
    calling wglGenlockSourceDelayI3D.

      BOOL wglGenlockSourceDelayI3D(HDC hDC,
                                    UINT uDelay)

    <uDelay> specifies the delay (in pixels) that the trigger is
    delayed before being used to synchronize the screen refresh.
    <uDelay> must be in the range [0, <maxDelay>] where <maxDelay>
    is the number of pixel clocks needed to display an entire frame.
    The maximum delay <maxDelay> can be calculated by the following
    equation:

          <maxDelay> = <maxLineDelay> * <maxPixelDelay>

    where <maxLineDelay> and <maxPixelDelay> can be queried by
    calling wglQueryGenlockMaxSourceDelayI3D.

      BOOL wglQueryGenlockMaxSourceDelayI3D(HDC hDC,
                                            UINT *uMaxLineDelay,
                                            UINT *uMaxPixelDelay)

    The current source delay can be queried by calling
    wglGetGenlockSourceDelayI3D.

    Genlock is enabled for each monitor by calling wglEnableGenlockI3D.

      BOOL wglEnableGenlockI3D(HDC hDC)

    Genlock is enabled for the monitor attached to the device with
    the device context <hDC> of a window created on the monitor.

    Genlock can be disabled for a monitor by calling
    wglDisableGenlockI3D.

      BOOL wglDisableGenlockI3D(HDC hDC)

    The current genlock enable can be queried by calling
    wglIsEnabledGenlockI3D.

    In order to avoid synchronization to an incomplete genlock
    specification, genlock should be disabled while the genlock
    parameters are being changed.  The exception to this is changing
    the genlock trigger delay with wglGenlockSourceDelayI3D.

Dependencies on WGL_EXT_extensions_string

    Because there is no way to extend wgl, these calls are defined in
    the ICD and can be called by obtaining the address with
    wglGetProcAddress.  Because this extension is a WGL extension, it
    is not included in the GL_EXTENSIONS string.  Its existence can be
    determined with the WGL_EXT_extensions_string extension.

Errors

    If any of the genlock functions succeed, a value of TRUE is
    returned.  If a function fails, a value of FALSE is returned.  To
    get extended error information, call GetLastError.

      ERROR_DC_NOT_FOUND         The <hDC> was not valid.

      ERROR_NO_SYSTEM_RESOURCES  The genlock functionality is not
                                 supported.

      ERROR_INVALID_DATA         <uSource> is not one of the valid
                                 sources.

      ERROR_INVALID_DATA         <uEdge> is not one of the valid
                                 source edge modes.

      ERROR_INVALID_DATA         <uRate> is less than a value of 1 or
                                 greater than a value of 6.

      ERROR_INVALID_DATA         <uDelay> is greater than <maxDelay>.

New State

    None

New Implementation Dependent State

    None

Revision History

    10/26/1999  0.1  First draft.
    04/17/2000  1.0  Released driver to ISVs.
"""
