# Copyright (c) 2006-2010 Mitch Garnaat http://garnaat.org/
# Copyright (c) 2010, Eucalyptus Systems, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from boto.cloudfront.signers import TrustedSigners

class CacheBehavior(object):
    """
    Cache behavior information to associate with the distribution.
    """

    def __init__(self, trusted_signers=None, origin_id=None, query_string=False, viewer_protocol_policy=None, min_ttl=None, default=False):
        """
        :param trusted_signers: Specifies any AWS accounts you want to
                                permit to create signed URLs for private
                                content. If you want the distribution to
                                use signed URLs, this should contain a
                                TrustedSigners object; if you want the
                                distribution to use basic URLs, leave
                                this None.
        :type trusted_signers: :class`boto.cloudfront.signers.TrustedSigners`

        :param query_string: True or False to forward query strings.
        :type query_string: bool
        
        :param viewer_protocol_policy: Restrict viewer access protocol type.
                                       allow-all
                                       https-only
        :type viewer_protocol_policy: str
        
        """
        self.default = default
        self.trusted_signers = trusted_signers
        self.origin_id = origin_id
        self.query_string = query_string
        self.viewer_protocol_policy = viewer_protocol_policy
        self.min_ttl = min_ttl

    def __repr__(self):
        container = 'DefaultCacheBehavior' if self.default else 'CacheBehavior'
        return '<%s: %s>' % (container, self.origin_id)

    def startElement(self, name, attrs, connection):
        if name == 'TrustedSigners':
            self.trusted_signers = TrustedSigners()
            return self.trusted_signers
        else:
            return None

    def endElement(self, name, value, connection):
        if name == 'TargetOriginId':
            self.origin_id = value
        elif name == 'QueryString':
            if value.lower() == 'true':
                self.query_string = True
            else:
                self.query_string = False
        elif name == 'ViewerProtocolPolicy':
            self.viewer_protocol_policy = value
        elif name == 'MinTTL':
            self.min_ttl = value
        else:
            setattr(self, name, value)

    def to_xml(self):
        container = 'DefaultCacheBehavior' if self.default else 'CacheBehavior'
        s = '  <%s>\n' % container
        s += '    <TargetOriginId>%s</TargetOriginId>\n' % self.origin_id
        s += '    <ForwardedValues>\n'
        s += '      <QueryString>%s</QueryString>\n' % ('true' if self.query_string else 'false')
        s += '    </ForwardedValues>\n'
        s += '<TrustedSigners>\n'
        s += '<Enabled>true</Enabled>\n'
        s += '<Quantity>%d</Quantity>\n' % (len(self.trusted_signers) if self.trusted_signers else 0)
        if self.trusted_signers:
            s += '<Items>\n'
            for signer in self.trusted_signers:
                #if signer == 'Self': signer = 'self'
                s += '  <AwsAccountNumber>%s</AwsAccountNumber>\n' % signer
            s += '</Items>\n'
        s += '</TrustedSigners>\n'
        if self.viewer_protocol_policy:
            s += '    <ViewerProtocolPolicy>%s</ViewerProtocolPolicy>\n' % self.viewer_protocol_policy
        if self.min_ttl:
            s += '    <MinTTL>%s</MinTTL>\n' % self.min_ttl
        s += '  </%s>\n' % container
        return s
